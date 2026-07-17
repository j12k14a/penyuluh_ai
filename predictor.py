from google import genai
import PIL.Image

# 1. PENTING: Jangan lupa isi ulang API Key Anda di sini
API_KEY = "AQ.Ab8RN6IdYaBvLyiJ02yYShEyZKvc8mEtbQpRi3QbfQPxzzZNlw"
client = genai.Client(api_key=API_KEY)

class PakarBotaniSession:
    def __init__(self, history_data=None):
        # Membuat sesi obrolan (chat) agar AI memiliki daya ingat 
        self.chat = client.chats.create(model='gemini-2.5-flash')
        
        if history_data:
            context = "Ini adalah riwayat obrolan kita sebelumnya mengenai analisis tanaman. Tolong ingat konteks ini:\n\n"
            for msg in history_data:
                if msg["sender"] in ["User", "AI"]:
                    sender_name = "Saya (Petani)" if msg["sender"] == "User" else "Kamu (Pakar Botani)"
                    context += f"[{sender_name}]: {msg['text']}\n\n"
            context += "PENTING: Jawab 'Siap' saja tanpa kalimat lain untuk mengonfirmasi bahwa kamu sudah mengingat konteks ini dan siap melanjutkan."
            
            try:
                self.chat.send_message(context)
            except:
                pass
        
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
