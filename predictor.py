from google import genai
import PIL.Image

# 1. PENTING: Jangan lupa isi ulang API Key Anda di sini
API_KEY = "ISI dengan Ur API KEY"
client = genai.Client(api_key=API_KEY)

class PakarBotaniSession:
    def __init__(self):
        # Membuat sesi obrolan (chat) agar AI memiliki daya ingat 
        self.chat = client.chats.create(model='gemini-2.5-flash')
        
    def predict_disease(self, image_path):
        try:
            img = PIL.Image.open(image_path)
            
            prompt_text = (
                "Kamu adalah pakar botani dan ahli penyakit tanaman. "
                "Tolong amati gambar daun/tanaman ini dengan sangat teliti. "
                "Berikan laporan analisis dalam bahasa Indonesia dengan struktur berikut:\n"
                "1. Identifikasi Tanaman: (Sebutkan nama spesies/jenis tanamannya)\n"
                "2. Status Kesehatan: (Apakah sehat, atau ada penyakit/kekurangan nutrisi?)\n"
                "3. Saran Penanganan: (Apa yang harus dilakukan pemiliknya?)"
            )

            # Kirim gambar dan prompt awal ke memori chat
            response = self.chat.send_message([prompt_text, img])
            return response.text

        except Exception as e:
            return f"Terjadi kesalahan saat menghubungi server Google: {str(e)}"
            
    def ask_follow_up(self, question):
        try:
            # Karena ini bagian dari memori chat, kita cukup mengirimkan teks pertanyaan tambahannya
            response = self.chat.send_message(question)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
