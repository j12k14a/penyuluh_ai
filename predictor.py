from google import genai # SDK Google Gemini
import PIL.Image # Library pembaca gambar

# 1. PENTING: Jangan lupa isi ulang API Key Anda di sini
API_KEY = "ISI dengan Ur API KEY"
client = genai.Client(api_key=API_KEY)

class PakarBotaniSession: # Class yang bertugas mengelola komunikasi dengan Gemini AI
    def __init__(self): # Method konstruktor Dipanggil otomatis saat object baru dibuat dari sebuah class dan digunakan untuk menetapkan nilai awal
        # Membuat sesi obrolan (chat) agar AI memiliki daya ingat 
        self.chat = client.chats.create(model='gemini-2.5-flash') # Membuat sesi chat baru yang memiliki memori percakapan.
        
    def predict_disease(self, image_path): # Method utama untuk menganalisis tanaman.
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
            return response.text # Mengembalikan hasil analisis ke GUI.

        except Exception as e:  # Menangkap semua jenis error yang mungkin terjadi  # str(e) digunakan untuk mengubah objek error menjadi teks  
            return f"Terjadi kesalahan saat menghubungi server Google: {str(e)}" # agar bisa ditampilkan ke pengguna
            
    def ask_follow_up(self, question):
        try:
            # Karena ini bagian dari memori chat, kita cukup mengirimkan teks pertanyaan tambahannya
            response = self.chat.send_message(question)
            return response.text 
        except Exception as e:
            return f"Error: {str(e)}"
