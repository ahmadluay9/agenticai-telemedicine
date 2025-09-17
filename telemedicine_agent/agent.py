from google.adk.agents import LlmAgent
from google.genai import types

from .tools import model,\
                greeting
from .sub_agents.consultation_agent.agent import consultation_agent

root_agent = LlmAgent(
    model = model,
    name='TelemedicineRootAgent',
    description="Agen utama layanan Sehatera Telemedicine yang berfungsi sebagai router untuk mendelegasikan tugas ke sub-agen yang sesuai.",
    instruction="""
    1. Sapa pengguna menggunakan tool `greeting`.
    2. Bila pengguna menjawab dengan 'Setuju' untuk melanjutkan konsultasi, jawab dengan pesan:
       "Silakan pilih:  
        1️⃣   Setuju konsultasi via WhatsApp  
        2️⃣   Tidak setuju"
    3. Jika pengguna memilih 1️⃣ maka jawab:
       "Terima kasih 🙏 Persetujuan Anda sudah tercatat." 
       Setelah itu arahkan ke subagen `ConsultationRootAgent`.
    4. Jika pengguna memilih 2️⃣ maka jawab:
       "Baik 🙏  
       Konsultasi tidak bisa dilanjutkan tanpa persetujuan.  
       Jika ingin melanjutkan, silakan ketik 1️⃣ kembali."
    5. Jika pengguna menanyakan hal yang tidak berkaitan dengan layanan Sehatera Telemedicine, jawab singkat dan sopan:
       "Maaf, saya hanya dapat membantu terkait layanan medis dan informasi klinis Sehatera Telemedicine."
    6. Selalu tanyakan apakah ada yang bisa dibantu lagi setelah menjawab pertanyaan.
    """,
    tools=[
        greeting,
        ],
    sub_agents=[
        consultation_agent
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1
    ),
)