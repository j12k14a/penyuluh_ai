# File ini berfungsi sebagai penghubung (interface) antara aplikasi kita dengan server AI (Google Gemini).
# Mengimpor library google-genai untuk berkomunikasi dengan model AI Google.
from google import genai
# Mengimpor modul Image dari PIL (Python Imaging Library) untuk memproses file gambar.
import PIL.Image

# Mendefinisikan konstanta (variabel statis) untuk menyimpan API Key rahasia kita.
API_KEY = "AQ........"

# Membuat objek klien (client) dari library genai menggunakan API key di atas.
client = genai.Client(api_key=API_KEY)

# Konsep OOP: Class
# Mendeklarasikan sebuah cetak biru bernama 'PakarBotaniSession'.
class PakarBotaniSession:
    
    # Konsep OOP: Constructor (Magic Method)
    # Method '__init__' ini dipanggil pertama kali secara otomatis ketika objek dibuat.
    def __init__(self, history_data=None):
        # Konsep OOP: Property / Atribut (Encapsulation)
        # Membuat instansi chat baru dari model gemini-2.5-flash dan menyimpannya di variabel instance 'self.chat'.
        self.chat = client.chats.create(model='gemini-2.5-flash')
        
        # Mengecek apakah ada data obrolan sebelumnya (history_data) yang dikirimkan.
        if history_data:
            # Membuat variabel string awal untuk menampung riwayat percakapan.
            context = "Ini adalah riwayat obrolan kita sebelumnya mengenai analisis tanaman. Tolong ingat konteks ini:\n\n"
            # Melakukan perulangan untuk setiap pesan di dalam data histori.
            for msg in history_data:
                # Memeriksa apakah pesan tersebut berasal dari "User" atau "AI".
                if msg["sender"] in ["User", "AI"]:
                    # Mengatur nama pengirim berdasarkan tipe pengirim (Ternary operator).
                    sender_name = "Saya (Petani)" if msg["sender"] == "User" else "Kamu (Pakar Botani)"
                    # Menambahkan teks pesan tersebut ke dalam variabel string konteks.
                    context += f"[{sender_name}]: {msg['text']}\n\n"
            # Menambahkan instruksi rahasia ke AI di akhir teks agar dia hanya membalas 'Siap'.
            context += "PENTING: Jawab 'Siap' saja tanpa kalimat lain untuk mengonfirmasi bahwa kamu sudah mengingat konteks ini dan siap melanjutkan."
            
            # Blok try-except untuk menangkap kemungkinan error (misal jaringan putus).
            try:
                # Mengirimkan seluruh konteks (riwayat lama) ke AI agar ia bisa mempelajarinya ulang.
                self.chat.send_message(context)
            # Penangkap error dari try di atas.
            except:
                # Jika gagal/error, lewati saja instruksinya tanpa membuat program crash (gagal diam-diam).
                pass
        
    # Konsep OOP: Method (Tingkah Laku / Behavior dari objek)
    # Method ini bertugas menerima path file gambar, memprosesnya, dan meminta prediksi penyakit ke AI.
    def predict_disease(self, image_path):
        # Memulai blok try untuk menangani error tak terduga.
        try:
            # Membuka file gambar secara lokal di komputer kita menggunakan objek PIL Image.
            img = PIL.Image.open(image_path)
            
            # Menyusun instruksi/perintah (prompt) awal untuk sistem pakar botani (AI).
            prompt_text = (
                # Kalimat pertama, memberikan persona "Pakar Botani".
                "Kamu adalah pakar botani dan ahli penyakit tanaman. "
                # Kalimat kedua, memerintahkan AI mengamati gambar secara teliti.
                "Tolong amati gambar daun/tanaman ini dengan sangat teliti. "
                # Kalimat ketiga, format output yang diwajibkan dalam Bahasa Indonesia.
                "Berikan laporan analisis dalam bahasa Indonesia dengan struktur berikut:\n"
                # Menuntut bagian poin 1 (Identifikasi).
                "1. Identifikasi Tanaman: (Sebutkan nama spesies/jenis tanamannya)\n"
                # Menuntut bagian poin 2 (Status Kesehatan).
                "2. Status Kesehatan: (Apakah sehat, atau ada penyakit/kekurangan nutrisi?)\n"
                # Menuntut bagian poin 3 (Saran).
                "3. Saran Penanganan: (Apa yang harus dilakukan pemiliknya?)"
            )

            # Konsep OOP: Abstraction
            # Mengirim prompt berupa list berisi [teks instruksi, gambar] ke model AI dan menuggu respons (blocking).
            response = self.chat.send_message([prompt_text, img])
            # Mengembalikan teks murni dari respons yang didapatkan dari Google AI ke pemanggil method.
            return response.text

        # Blok penangkap error jika proses di atas gagal.
        except Exception as e:
            # Mengembalikan teks pesan error sistem agar ditampilkan di layar pengguna alih-alih merusak program.
            return f"Terjadi kesalahan saat menghubungi server Google: {str(e)}"
            
    # Konsep OOP: Method tambahan untuk fitur tanya jawab lanjutan (Follow-up)
    # Method ini dipanggil saat pengguna menanyakan teks biasa setelah gambar dianalisis.
    def ask_follow_up(self, question):
        # Memulai blok perlindungan error jaringan/API.
        try:
            # Mengirimkan teks pertanyaan ke AI. Karena dikirim ke sesi chat yang sama, AI tetap mengingat foto daunnya.
            response = self.chat.send_message(question)
            # Mengembalikan jawaban dari AI.
            return response.text
        # Jika terjadi masalah pengiriman pesan (misalnya timeout internet).
        except Exception as e:
            # Mengembalikan string error sistem.
            return f"Error: {str(e)}"
