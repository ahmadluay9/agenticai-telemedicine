from google.adk.agents import LlmAgent
from google.genai import types
from ...tools import model

consultation_agent = LlmAgent(
    model = model,
    name='ConsultationRootAgent',
    description="Agen .",
    instruction="""
    1. Tampilkan Catatan Penting sebelum konsultasi:
         "# Catatan Penting
📌 Layanan ini: \n
✔️ Hanya untuk **pasien usia ≥8 tahun** \n
✔️ Hanya untuk kasus non-darurat \n
\n
⚠️ Segera ke IGD/RS terdekat bila mengalami:
\n
1. **Gangguan Pernapasan** → sesak berat, napas berhenti, tersedak \n
2. **Nyeri Dada** → menekan/menjalar, dengan keringat dingin/pingsan \n
3. **Gangguan Pencernaan** → muntah >3x + diare >4x, atau diare cair >6x \n
4. **Penurunan Kesadaran** → pingsan, sulit dibangunkan, kejang berulang \n
5. **Trauma / Cedera Berat** → patah tulang, cedera kepala, luka bakar luas \n
6. **Gejala Stroke** → mulut mencong, bicara pelo, lemas separuh badan \n
7. **Demam Tinggi + Bahaya** → >39°C dengan kaku kuduk, ruam, kejang \n
8. **Reaksi Alergi Berat (Anafilaksis)** → bengkak wajah/tenggorokan, sesak, tekanan darah turun \n
9. **Keracunan** → obat/zat berbahaya, gas beracun \n
10. **Ibu Hamil kondisi Darurat** → perdarahan banyak, kejang (eklamsia), ketuban pecah dini + demam/nyeri \n
11. **Perdarahan Hebat** → muntah darah, BAB hitam, luka dalam kecelakaan \n

--- 

Informasi Legal
📝 1.NIB: 26082500610977 \n
📖 2.Regulasi: UU No.29/2004 Pasal 52(c) & Permenkes 290/2008 Pasal 7(3) \n
📖 3.Regulasi :*“Mengacu pada UU Perlindungan Data Pribadi (UU No.27/2022)”* "

    """,
    # tools=[
    #     greeting,
    #     ],
    # sub_agents=[
    #     consultation_agent
    # ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1
    ),
)