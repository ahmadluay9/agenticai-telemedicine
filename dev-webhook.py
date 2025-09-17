import os
import uvicorn
from pyngrok import ngrok
from dotenv import load_dotenv

def main():
    """
    Memulai tunnel ngrok lalu menjalankan aplikasi FastAPI.
    Skrip ini ditujukan untuk keperluan pengembangan saja.
    """
    load_dotenv()

    port = int(os.environ.get("PORT", 8080))
    ngrok_auth_token = os.environ.get("NGROK_AUTH_TOKEN")

    if not ngrok_auth_token:
        print("Error: Variabel lingkungan NGROK_AUTH_TOKEN belum diatur.")
        print("Silakan dapatkan token Anda dari https://dashboard.ngrok.com/get-started/your-authtoken")
        print("dan tambahkan ke file .env Anda.")
        return

    # Atur token autentikasi ngrok
    ngrok.set_auth_token(ngrok_auth_token)

    try:
        # Buka tunnel ngrok baru
        public_url = ngrok.connect(port, "http").public_url
        print("=" * 70)
        print(f"🚀 Terowongan ngrok aktif di: {public_url}")
        print(f"🔗 URL webhook Twilio Anda adalah: {public_url}/whatsapp")
        print("=" * 70)
        print(f"Memulai server Uvicorn di port {port}...")

        # Jalankan aplikasi FastAPI menggunakan Uvicorn
        # String 'main:app' memberitahu Uvicorn di mana menemukan instance FastAPI
        uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        # Putuskan koneksi ngrok saat aplikasi dihentikan
        all_tunnels = ngrok.get_tunnels()
        if all_tunnels:
             print("Menutup terowongan ngrok.")
             ngrok.disconnect(all_tunnels[0].public_url)
        ngrok.kill()

if __name__ == "__main__":
    main()