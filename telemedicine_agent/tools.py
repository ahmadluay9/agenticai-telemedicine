import os
from dotenv import load_dotenv

load_dotenv()

model = os.environ.get("MODEL")

# def greeting():
#     return """Halo 👋, selamat datang di **SEHATERA TELEMEDICINE**\n
#     Layanan kesehatan online untuk Anda dan keluarga.\n
#     👩‍⚕️. Konsultasi dilakukan online, ada keterbatasan pemeriksaan fisik.\n
#  Bila perlu resep **Obat Keras Tertentu (OKT)** diluar area Malang, bisa minta tolong resep OKT melalui dokter/Puskesmas setempat (mungkin ada biaya tambahan).\n
#     \n
#     📞 **ADMIN : 0851 7711 6550** \n
#     ✅ Pendaftaran\n
#     ✅ Jadwal Konsultasi\n
#     ✅ Pembayaran Resmi\n
#     ✅ Terhubung dengan Admin & Sistem
#     \n
#     \n
#     📞 **VIP (Berbayar): 0851 8366 5758**\n
#     📢 Jawaban Konsultasi dan Edukasi kesehatan \n
#     🤝 Tindak lanjut / Follow-up \n
#     💬 Komunikasi personal\n
#     ⚠️ Bukan untuk pendaftaran/pembayaran resmi \n
# \n
#     Sebelum konsultasi dimulai, mohon baca penjelasan berikut:
# \n
#     📌 Konsultasi dilakukan online (WhatsApp), sehingga ada keterbatasan pemeriksaan fisik.\n
#     📌 Data medis Anda dijaga kerahasiaannya sesuai Kode Etik Kedokteran & regulasi yang berlaku.\n
#     📌 Jika diperlukan, Anda dapat dirujuk ke dokter, laboratorium, atau fasilitas kesehatan terkait.\n
#     📌 Informasi yang diberikan bersifat pendukung, bukan pengganti pemeriksaan medis langsung.\n
#     📌 Untuk kondisi gawat darurat, segera menuju IGD atau faskes terdekat.\n
# \n
#     Berbasis regulasi :\n
#     - UU No. 29 Tahun 2004 (Praktik Kedokteran) \n
#     - Permenkes No. 290 Tahun 2008 (Persetujuan Tindakan Kedokteran) \n
#     - Permenkes No. 20 Tahun 2019 (Telemedicine)\n
#     \n
#     Jika Anda mengirim pesan di luar jam konsultasi, balasan akan diberikan pada jam layanan berikutnya.\n
#  Terima kasih atas pengertiannya 🙏\n
# \n
#     👉 Dengan melanjutkan konsultasi ini, Anda menyatakan telah membaca & memahami penjelasan di atas.\n
#     Jika Anda setuju, silakan balas dengan:\n
#     SETUJU ✅
#     """

def greeting():
    return """Halo 👋, selamat datang di **SEHATERA TELEMEDICINE**\n
    👉 Dengan melanjutkan konsultasi ini, Anda menyatakan telah membaca & memahami penjelasan di atas.\n
    Jika Anda setuju, silakan balas dengan:\n
    SETUJU ✅
    """