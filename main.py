import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Response, Request, Header, HTTPException
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

# Impor ADK dan GenAI
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

# Impor agen utama Anda
from telemedicine_agent.agent import root_agent

# Muat environment variables dari file .env
load_dotenv()

# --- Konfigurasi Twilio ---
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
if not TWILIO_AUTH_TOKEN:
    raise ValueError("TWILIO_AUTH_TOKEN environment variable not set!")
validator = RequestValidator(TWILIO_AUTH_TOKEN)


# --- Konfigurasi dan Inisialisasi ADK Runner ---
def setup_adk_runner():
    """Menginisialisasi dan mengembalikan Runner ADK dan session service."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="telemedice_whatsapp_app",
        session_service=session_service
    )
    return runner, session_service

runner, session_service = setup_adk_runner()
app = FastAPI()

# Set untuk melacak sesi yang sudah dibuat agar tidak perlu dibuat ulang.
# Catatan: Pendekatan ini hanya cocok untuk InMemorySessionService
# dan saat menjalankan aplikasi dengan satu worker.
created_sessions = set()

## --- Fungsi Ekstraksi ---
def extract_text_response(content: genai_types.Content) -> str | None:
    """Ekstrak teks dari respons ADK (abaikan non-text parts)."""
    if not content or not content.parts:
        return None

    response_parts = []
    for part in content.parts:
        # Kalau part punya teks biasa
        if getattr(part, "text", None):
            response_parts.append(part.text.strip())

        # Kalau part berupa function_response dengan field result
        elif getattr(part, "function_response", None):
            func_resp_content = part.function_response.response
            if func_resp_content and "result" in func_resp_content:
                result_text = func_resp_content["result"]
                if isinstance(result_text, str):
                    response_parts.append(result_text.strip())

    if not response_parts:
        return None

    # Gabungkan semua part jadi satu string
    full_text = "\n".join(response_parts)

    # Convert markdown **bold** ke *bold* biar sesuai format WhatsApp
    return full_text.replace("**", "*").strip()


# --- Fungsi Asinkron untuk Menjalankan Agen ---
async def dapatkan_respons_agen_async(prompt: str, user_id: str):
    """Menjalankan agen ADK secara asinkron dan mengembalikan respons akhir."""
    session_id = user_id

    # Periksa cache lokal. Jika sesi belum pernah dibuat untuk user ini,
    # buat sesi baru secara eksplisit.
    if session_id not in created_sessions:
        try:
            print(f"Membuat sesi baru untuk user: {user_id}")
            await session_service.create_session(
                app_name=runner.app_name, user_id=user_id, session_id=session_id
            )
            created_sessions.add(session_id)
        except Exception as e:
            print(f"ERROR: Gagal membuat sesi untuk {user_id}: {e}")
            return "Maaf, terjadi masalah saat memulai percakapan. Silakan coba lagi nanti."

    content = genai_types.Content(role='user', parts=[genai_types.Part(text=prompt)])
    teks_respons_akhir = "Maaf, terjadi kesalahan saat memproses permintaan Anda."

    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            if event.is_final_response():
                print("DEBUG: Raw final event content:", event.content)
                extracted_text = extract_text_response(event.content)
                if extracted_text:
                    teks_respons_akhir = extracted_text
                break
    except Exception as e:
        print(f"ERROR: Terjadi kesalahan saat menjalankan runner ADK: {e}")
        # Hapus sesi dari cache jika terjadi error agar bisa dibuat ulang pada request berikutnya
        if session_id in created_sessions:
            created_sessions.remove(session_id)

    return teks_respons_akhir

# --- Endpoint FastAPI ---
@app.post("/whatsapp")
async def whatsapp_reply(request: Request, x_twilio_signature: str = Header(None)):
    """Merespons pesan WhatsApp yang masuk SETELAH memvalidasi request."""
    
    # Rekonstruksi URL publik untuk validasi di lingkungan proxy seperti Cloud Run
    protocol = request.headers.get("x-forwarded-proto", "https")
    host = request.headers.get("host")
    url = f"{protocol}://{host}{request.url.path}"

    # Validasi permintaan dari Twilio
    form_params = await request.form()
    is_valid_request = validator.validate(
        url,
        form_params,
        x_twilio_signature or ''
    )
    
    if not is_valid_request:
        print(f"Validation failed. URL used: {url}")
        raise HTTPException(status_code=403, detail="Request not from Twilio")

    incoming_msg = form_params.get('Body')
    sender_number = form_params.get('From')
    
    print(f"Pesan dari {sender_number}: {incoming_msg}")

    agent_response_text = await dapatkan_respons_agen_async(
        prompt=incoming_msg, 
        user_id=sender_number
    )

    # Buat balasan TwiML
    resp = MessagingResponse()
    resp.message(agent_response_text)

    return Response(content=str(resp), media_type="application/xml")

# --- Menjalankan Aplikasi (untuk development) ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)