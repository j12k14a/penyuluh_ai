# Import library standar dan pihak ketiga yang dibutuhkan aplikasi
# tk: Modul utama tkinter untuk membuat Graphical User Interface (GUI)
import tkinter as tk
# filedialog: Membuka jendela pemilihan file, messagebox: Menampilkan pesan peringatan/error
from tkinter import filedialog, messagebox, simpledialog
# PIL (Pillow): Library untuk manipulasi dan pemrosesan gambar tingkat lanjut
from PIL import Image, ImageTk
# threading: Mengizinkan proses berjalan di latar belakang (background) agar GUI tidak hang
import threading
# re: Library Regular Expression, digunakan di sini untuk mengatur format teks tebal (bold)
import re
# cv2: OpenCV, library canggih untuk pemrosesan gambar dan akses kamera (webcam)
import cv2
# predictor: Modul buatan sendiri yang berisi class PakarBotaniSession (Konsep Modular Programming)
import predictor  
# os: Berinteraksi dengan sistem operasi, misalnya mengecek keberadaan file
import os
# json: Mengubah data struktur Python (Dictionary/List) ke format file JSON dan sebaliknya
import json
# datetime: Modul waktu, dipakai untuk mendapatkan jam saat membuat judul riwayat histori
import datetime

# Konstanta Tema (Variabel global statis)
# Digunakan untuk mendefinisikan warna dan font standar yang digunakan secara konsisten di seluruh aplikasi
BG_COLOR = "#F1F8E9"         # Warna hijau sangat muda untuk latar belakang utama
PRIMARY_COLOR = "#2E7D32"    # Warna hijau tua untuk tombol aksi utama
SECONDARY_COLOR = "#A5D6A7"  # Warna hijau sedang untuk kolom panel samping
TEXT_COLOR = "#1B5E20"       # Warna teks hijau paling gelap
FONT_TITLE = ("Segoe UI", 26, "bold") # Font untuk judul aplikasi
FONT_NORMAL = ("Segoe UI", 12)        # Font ukuran normal
FONT_RESULT = ("Segoe UI", 12)        # Font khusus untuk teks obrolan/hasil analisis

# Konsep OOP: Class
# Class ini berfungsi sebagai "Blueprint" (cetak biru) atau kerangka utama dari seluruh Antarmuka (GUI).
# Class ini membungkus semua elemen antarmuka (Encapsulation) menjadi satu objek aplikasi mandiri.
class PenyuluhAIApp:
    
    # Konsep OOP: Constructor (__init__)
    # Method otomatis yang akan dipanggil saat kita pertama kali membuat instansi dari class ini.
    # Berfungsi untuk menginisialisasi atribut atau "state" awal objek.
    def __init__(self, root):
        # Atribut objek (instance variables)
        self.root = root  # Menyimpan window (layar) utama Tkinter
        # Menentukan judul window aplikasi
        self.root.title("Penyuluh-AI: Sistem Pakar Botani Interaktif")
        # Mengatur ukuran awal window aplikasi (lebar x tinggi)
        self.root.geometry("1000x900")
        # Mengatur warna latar belakang keseluruhan window
        self.root.configure(bg=BG_COLOR)
        
        # Variabel untuk menyimpan path/lokasi file gambar yang dipilih user
        self.image_path = None
        # Konsep OOP: Komposisi Objek
        # Menginstansiasi objek dari class eksternal (PakarBotaniSession) sebagai atribut dari class ini.
        self.ai_session = None  
        # Kunci (judul) sesi yang sedang aktif saat ini, misalnya "Analisis: 21:00:00"
        self.current_session_key = None
        # Atribut dictionary untuk menyimpan memori histori semua percakapan
        self.history_data = {}  
        
        # Memanggil method internal 'create_widgets' untuk langsung menggambar tombol dan teks di layar
        self.create_widgets()
        
    # Konsep OOP: Method pembantu (UI Builder)
    # Bertugas membuat dan menyusun tata letak (layout) semua komponen antarmuka GUI.
    def create_widgets(self):
        # Membuat frame/container raksasa untuk menampung seluruh layout 3 kolom
        content_frame = tk.Frame(self.root, bg=BG_COLOR)
        # Menempelkan frame tersebut ke window utama dengan jarak margin
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ----------------- KOLOM KIRI (Menu Utama) -----------------
        # Membuat frame kiri untuk tombol menu dan preview gambar
        left_frame = tk.Frame(content_frame, bg=SECONDARY_COLOR, width=280)
        # Meletakkannya merapat ke kiri (side=tk.LEFT)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        # Mencegah frame menyusut mengecil mengikuti isinya (tetap pada lebar 280)
        left_frame.pack_propagate(False)

        # Membuat teks label sebagai judul aplikasi di panel kiri
        title_label = tk.Label(left_frame, text="🌿 Penyuluh-AI", font=("Segoe UI", 20, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR)
        # Menempelkan judul dengan jarak margin (pady)
        title_label.pack(pady=20)
        
        # Membuat label berbentuk kotak yang akan berfungsi menampung/menampilkan foto tanaman
        self.image_label = tk.Label(left_frame, bg="white", text="Pratinjau Gambar", font=FONT_NORMAL, width=30, height=12)
        # Menempelkan kotak foto tersebut
        self.image_label.pack(pady=10, padx=10)
        
        # Membuat tombol "Pilih Foto", jika di-klik akan menjalankan method self.select_image
        self.btn_select = tk.Button(left_frame, text="📁 Pilih Foto", font=("Segoe UI", 11, "bold"), bg=PRIMARY_COLOR, fg="white", command=self.select_image)
        # Melebarkan tombol memenuhi layar (fill=tk.X)
        self.btn_select.pack(fill=tk.X, padx=20, pady=5)

        # Membuat tombol "Buka Kamera", jika di-klik akan memanggil method self.open_camera
        self.btn_camera = tk.Button(left_frame, text="📸 Buka Kamera", font=("Segoe UI", 11, "bold"), bg=PRIMARY_COLOR, fg="white", command=self.open_camera)
        self.btn_camera.pack(fill=tk.X, padx=20, pady=5)

        # Membuat tombol "Mulai Analisis". Awalnya tombol ini dinonaktifkan (state=DISABLED) sampai gambar dipilih
        self.btn_analyze = tk.Button(left_frame, text="🔍 Mulai Analisis", font=("Segoe UI", 11, "bold"), bg="#FFB300", fg="black", command=self.start_analysis, state=tk.DISABLED)
        self.btn_analyze.pack(fill=tk.X, padx=20, pady=15)
        
        # Label teks untuk indikator "Loading..." saat AI sedang berpikir
        self.lbl_loading = tk.Label(left_frame, text="", font=("Segoe UI", 11, "italic"), bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        self.lbl_loading.pack()

        # Membuat sebuah frame/pembatas kosong untuk mendorong elemen logo ke bagian paling bawah kolom
        spacer = tk.Frame(left_frame, bg=SECONDARY_COLOR)
        spacer.pack(fill=tk.BOTH, expand=True)

        # Blok pelindung try-except untuk mencegah error jika file logo tidak sengaja terhapus
        try:
            # Memeriksa eksistensi file logo di direktori program
            if os.path.exists("logo_app.png"):
                # Membuka logo menggunakan PIL
                logo_pil = Image.open("logo_app.png")
                # Mengonversi gambar PIL menjadi format yang dimengerti oleh Tkinter
                self.logo_img = ImageTk.PhotoImage(logo_pil)
                # Membuat Label yang diisi dengan objek gambar logo
                self.lbl_logo = tk.Label(left_frame, image=self.logo_img, bg=SECONDARY_COLOR)
                # Menempelkan logo di paling dasar kolom (side=tk.BOTTOM)
                self.lbl_logo.pack(side=tk.BOTTOM, pady=(0, 20))
        except Exception:
            # Lewati (abaikan) jika ada error saat memuat logo
            pass

        # Membuat teks keterangan Hak Cipta / Kreator Aplikasi
        self.lbl_watermark = tk.Label(left_frame, text="Builder by Kelompok 6 PBO", font=("Segoe UI", 10, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR)
        # Menempelkan watermark juga di bawah (di atas logo karena di-pack setelah logo)
        self.lbl_watermark.pack(side=tk.BOTTOM, pady=(10, 5))


        # ----------------- KOLOM TENGAH (Ruang Diskusi & Chat) -----------------
        # Membuat frame tengah yang mengambil seluruh sisa ruang kosong (expand=True)
        middle_frame = tk.Frame(content_frame, bg=BG_COLOR)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Label Judul Kolom Tengah
        middle_title = tk.Label(middle_frame, text="Ruang Diskusi & Hasil", font=("Segoe UI", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        middle_title.pack(pady=10)

        # Membuat kotak input teks berlapis (Text Box) untuk menampung riwayat percakapan/hasil
        self.txt_result = tk.Text(middle_frame, font=FONT_RESULT, wrap=tk.WORD, bg="white")
        # Melebarkannya ke segala arah
        self.txt_result.pack(fill=tk.BOTH, expand=True)
        
        # Mengonfigurasi beberapa "Tag" gaya huruf di text box:
        # Tag 'bold' untuk huruf tebal dari AI
        self.txt_result.tag_configure('bold', font=("Segoe UI", 12, "bold"), foreground=PRIMARY_COLOR)
        # Tag 'normal' untuk teks biasa
        self.txt_result.tag_configure('normal', font=FONT_RESULT)
        # Tag 'user' untuk teks input dari user (berwarna biru, rata kanan, cetak miring)
        self.txt_result.tag_configure('user', font=("Segoe UI", 12, "italic"), foreground="blue", justify='right')
        
        # Menambahkan bilah penggulung (Scrollbar) vertikal ke text box
        scrollbar = tk.Scrollbar(self.txt_result)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Menghubungkan scrollbar dengan mekanisme scroll pada text box
        self.txt_result.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.txt_result.yview)

        # Membuat baris input khusus tempat pengguna mengetikkan pertanyaannya
        chat_input_frame = tk.Frame(middle_frame, bg=BG_COLOR, pady=10)
        chat_input_frame.pack(fill=tk.X)
        
        # Kolom input teks sederhana (satu baris)
        self.entry_chat = tk.Entry(chat_input_frame, font=FONT_NORMAL)
        # Ditempel merapat kiri
        self.entry_chat.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        # Konsep OOP: Binding (Penghubungan Event). 
        # Jika user menekan tombol "Enter" (Return) di keyboard, maka panggil method send_chat.
        self.entry_chat.bind("<Return>", lambda event: self.send_chat())
        
        # Tombol "Tanya" untuk mengirim isi kolom input ke AI
        self.btn_send = tk.Button(chat_input_frame, text="Tanya", bg=PRIMARY_COLOR, fg="white", font=("Segoe UI", 10, "bold"), command=self.send_chat, state=tk.DISABLED)
        self.btn_send.pack(side=tk.RIGHT, padx=5)


        # ----------------- KOLOM KANAN (Menu Ekstra & Histori) -----------------
        # Membuat frame kanan berukuran lebar statis 250
        right_frame = tk.Frame(content_frame, bg=SECONDARY_COLOR, width=250)
        # Ditempel merapat ke tepi kanan layar
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        right_frame.pack_propagate(False)
        
        # Label judul untuk menu kanan
        right_title = tk.Label(right_frame, text="Menu Lanjutan", font=("Segoe UI", 14, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR)
        right_title.pack(pady=20)
        
        # Tombol untuk mengekspor isi obrolan ke file TXT. Akan memanggil method export_report.
        self.btn_export = tk.Button(right_frame, text="💾 Simpan Laporan", font=("Segoe UI", 11, "bold"), bg="#E64A19", fg="white", command=self.export_report, state=tk.DISABLED)
        self.btn_export.pack(fill=tk.X, padx=20, pady=10)
        
        # Judul label untuk area Histori
        history_title = tk.Label(right_frame, text="Histori Penyuluhan", font=("Segoe UI", 12, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR)
        history_title.pack(pady=(20, 5))
        
        # Listbox adalah widget tabel-list satu kolom untuk menampilkan daftar judul histori chat
        self.history_listbox = tk.Listbox(right_frame, font=FONT_NORMAL)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar khusus untuk daftar histori di Listbox
        hist_scrollbar = tk.Scrollbar(self.history_listbox)
        hist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Menghubungkan scrollbar tersebut ke yview milik Listbox
        self.history_listbox.config(yscrollcommand=hist_scrollbar.set)
        hist_scrollbar.config(command=self.history_listbox.yview)
        
        # Konsep OOP: Memanggil method internal class sendiri menggunakan sintaks self.[method]
        # Saat UI selesai dimuat, paksa aplikasi membaca file histori dari hardisk (jika ada).
        self.load_history()
        # Jika salah satu item di listbox diklik oleh user, jalankan fungsi 'on_history_select'.
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)


    # Konsep OOP: Encapsulation pada I/O File (Manajemen Data Histori)
    # Method khusus untuk memuat database histori berformat JSON dari hardisk ke dalam Listbox GUI.
    def load_history(self):
        # Memeriksa apakah file history_data.json sudah pernah dibuat
        if os.path.exists("history_data.json"):
            # Blok perlindungan try agar tidak crash apabila isi JSON corrupt
            try:
                # Buka file dalam mode baca "r" (Read)
                with open("history_data.json", "r", encoding="utf-8") as f:
                    # Parsing teks file JSON menjadi kamus (Dictionary) Python 
                    self.history_data = json.load(f)
                
                # Mengulang setiap kunci (judul histori/tanggal) dari dictionary data tersebut
                for key in self.history_data:
                    # Memasukkan judul tersebut ke Listbox layar satu per satu
                    self.history_listbox.insert(tk.END, key)
            except Exception as e:
                pass

    # Method untuk menimpa/menulis (Save) dictionary histori ke file hardisk JSON secara utuh.
    def save_history_data(self):
        # Buka (atau timpa) file dengan mode tulis "w" (Write)
        with open("history_data.json", "w", encoding="utf-8") as f:
            # Gunakan fungsi bawaan dump dari library json
            json.dump(self.history_data, f, indent=4)


    # Konsep OOP: Event Handler Method
    # Method ini dijalankan otomatis (listener) oleh aplikasi ketika terjadi aktivitas (event)
    # aktivitas tersebut adalah saat user me-klik salah satu judul histori di sebelah kanan.
    def on_history_select(self, event):
        # Dapatkan ID indeks dari listbox yang sedang di-klik/dipilih
        selection = self.history_listbox.curselection()
        # Batalkan bila kosong/salah klik
        if not selection: return
        # Ambil nilai indeks paling awal (karena bisa multiselect, kita butuh elemen [0])
        idx = selection[0]
        # Ambil nama kunci teks (string) berdasarkan posisi indeks
        session_key = self.history_listbox.get(idx)
        
        # Validasi apakah nama kunci valid (terdapat di memory aplikasi)
        if session_key in self.history_data:
            # Update key sesi berjalan dengan histori yang dipilih
            self.current_session_key = session_key
            # Bersihkan dulu area obrolan teks di layar utama
            self.clear_chat()
            
            # Memuat/merender semua baris riwayat obrolan (chat log) masa lalu ke UI kembali
            for msg in self.history_data[session_key]:
                # save=False mencegah fungsi ini untuk menyimpan ulang apa yang sudah ia tulis
                self.insert_chat_text(msg["sender"], msg["text"], save=False)
            
            # Nonaktifkan area input selama proses muat ulang model memakan waktu di server Google
            self.btn_send.config(state=tk.DISABLED)
            self.entry_chat.config(state=tk.DISABLED)
            self.lbl_loading.config(text="Memuat ulang memori percakapan...")
            
            # Konsep OOP + Concurrency: Menjalankan task di Thread (jalur) berbeda (Asynchronous)
            # Karena merekonstruksi API chat butuh beberapa detik internet, kita taruh di Thread 
            # agar seluruh jendela aplikasi GUI tidak macet ("Not Responding") karena menunggunya selesai.
            threading.Thread(target=self.reconstruct_session, args=(self.history_data[session_key],), daemon=True).start()

    # Method internal untuk membangun ulang (Rebuild) state memori dari objek class eksternal AI
    def reconstruct_session(self, history_list):
        # Konsep OOP: Menginstansiasi objek AI (PakarBotaniSession) kembali,
        # tapi kali ini kita mengirim parameter `history_list` agar model bisa "mengingat" masa lalunya
        self.ai_session = predictor.PakarBotaniSession(history_data=history_list)
        # Setelah selesai melakukan fetch server di Thread latar, eksekusi pembaruan UI (Thread utama)
        self.root.after(0, self.update_gui_after_reconstruct)
        
    # Method sinkronisasi GUI: Mengembalikan akses user ke menu sesaat setelah rekonstruksi berhasil
    def update_gui_after_reconstruct(self):
        # Kosongkan label indikator loading
        self.lbl_loading.config(text="")
        # Hidupkan kembali semua tombol menu dan input chat (state=NORMAL)
        self.btn_send.config(state=tk.NORMAL)
        self.entry_chat.config(state=tk.NORMAL)
        self.btn_export.config(state=tk.NORMAL)

    # Method untuk menangani proses user memilih gambar dari Windows File Explorer/Linux GUI
    def select_image(self):
        # Tampilkan pop-up pencari berkas khusus file berekstensi tipe Gambar
        filepath = filedialog.askopenfilename(filetypes=[('Gambar', '*.png *.jpg *.jpeg *.bmp')])
        # Jika user benar memilih gambar dan tidak membatalkan operasi
        if filepath:
            # Simpan path gambar ke properti aplikasi
            self.image_path = filepath
            # Tampilkan foto tersebut ke frame layar kiri
            self.display_image(filepath)
            # Karena foto sudah valid, hidupkan fungsi "Mulai Analisis"
            self.btn_analyze.config(state=tk.NORMAL)
            # Reset informasi memori/kunci histori (karena ini akan menjadi topik baru)
            self.current_session_key = None
            # Hapus chat lama sebelumnya (jika ada)
            self.clear_chat()
            # Berikan ucapan panduan oleh Sistem.
            self.insert_chat_text("Sistem", "Foto dimuat dari galeri. Klik 'Mulai Analisis'!")

    # Method yang menggunakan OpenCV (cv2) untuk menangkap jepretan kamera langsung (Webcam)
    def open_camera(self):
        # Indeks 0 biasanya merepresentasikan webcam utama di komputer/laptop
        cap = cv2.VideoCapture(0)
        
        # Mengecek jikalau hardware kamera diblokir / tidak ada drivernya
        if not cap.isOpened():
            messagebox.showerror("Error Kamera", "Kamera tidak ditemukan atau ditolak aksesnya oleh sistem operasi.")
            return
            
        import time
        # Proses "pemanasan" lensa kamera. Kamera seringkali gelap di awal nyala, 
        # sehingga kita membaca dan membuang 15 frame kotor pertama
        for _ in range(15):
            cap.read()
            time.sleep(0.05)
            
        # Membaca/menjepret frame final yang akan digunakan
        ret, frame = cap.read()
        if ret:
            # Menyimpan gambar yang dijepret menjadi file bernama temp_camera.jpg
            temp_path = "temp_camera.jpg"
            cv2.imwrite(temp_path, frame)
            
            # Memproses logic aplikasi sama halnya dengan user memilih foto biasa di menu "Pilih Foto"
            self.image_path = temp_path
            self.display_image(temp_path)
            self.btn_analyze.config(state=tk.NORMAL)
            self.current_session_key = None
            self.clear_chat()
            self.insert_chat_text("Sistem", "Foto berhasil diambil dari kamera. Klik 'Mulai Analisis'!")
        else:
            # Tampilkan peringatan jika terjadi malfungsi saat memproses jepretan
            messagebox.showerror("Error", "Gagal menangkap gambar dari kamera.")
        
        # Matikan komponen kamera (mematikan lampu indikator webcammnya)
        cap.release()

    # Method internal untuk menampilkan file path gambar ke dalam Label Tkinter di UI
    def display_image(self, path):
        try:
            # Baca path menjadi objek Image PIL
            img = Image.open(path)
            # Perkecil gambar agar pas secara proporsional untuk ditampilkan di UI (max 450x450 piksel)
            img.thumbnail((450, 450), Image.Resampling.LANCZOS)
            # Ubah ke objek PhotoImage yang dimengerti framework GUI Tkinter
            photo = ImageTk.PhotoImage(img)
            
            # Gantikan isi dan hilangkan teks kosong di label pratinjau gambar 
            self.image_label.config(image=photo, text="", width=450, height=450)
            # Perlindungan Reference (Reference Protection). 
            # Wajib ditulis agar gambar tidak dihapus otomatis oleh sistem pembersih memori Python (Garbage Collector).
            self.image_label.image = photo  
        except Exception as e:
            pass

    # Method untuk membersihkan seluruh riwayat tulisan yang nampak di kolom Chat Diskusi (Reset Layar)
    def clear_chat(self):
        # Aktifkan Text Box (karena awalnya dikunci/Read-Only)
        self.txt_result.config(state=tk.NORMAL)
        # Menghapus isinya dari baris pertama indeks 1.0 (karakter pertama) sampai END (akhir teks)
        self.txt_result.delete(1.0, tk.END)
        # Mengunci kembali Text Box (Read-Only) agar tidak bisa diubah langsung oleh user lewat keyboard
        self.txt_result.config(state=tk.DISABLED)

    # Method inti yang mengatur teknik *rendering* tata cara cetak obrolan/teks ke layar Chat
    def insert_chat_text(self, sender, text, save=True):
        # Buka paksa kunci blokir read-only sebelum dicetak 
        self.txt_result.config(state=tk.NORMAL)
        
        # Fitur simpan ke Histori aktif: jika fungsi sedang ditugaskan dan ada kunci histori 
        if save and self.current_session_key:
            # Jika kunci sesi ini belum ada di data history dictionary, maka buat wadah array/list kosong baru
            if self.current_session_key not in self.history_data:
                self.history_data[self.current_session_key] = []
            
            # Simpan barisan (Append) pesan ke memori aplikasi menggunakan format Object/Dictionary
            self.history_data[self.current_session_key].append({"sender": sender, "text": text})
            # Langsung sinkronisasikan/tulis datanya ke hardisk lewat JSON (Autosave)
            self.save_history_data()
        
        # Pengecekan tipe pesan berdasarkan pengirim (sender):
        # 1. Pesan User
        if sender == "User":
            # Mencetak menggunakan tag 'user' (rata kanan miring biru seperti dideklarasikan di awal)
            self.txt_result.insert(tk.END, f"\nAnda:\n{text}\n\n", 'user')
        
        # 2. Pesan Sistem 
        elif sender == "Sistem":
            # Dicetak menggunakan 'normal' (tulisan informatif sistem berwarna hitam biasa)
            self.txt_result.insert(tk.END, f"\n[INFO] {text}\n", 'normal')
        
        # 3. Pesan AI (Pakar Botani)
        else: 
            # Mencetak heading pembuka berhuruf tebal
            self.txt_result.insert(tk.END, f"\n--- Pakar Botani ---\n", 'bold')
            # Memperbaiki formatting Markdown Gemini dari asteris biasa ke bullet
            text = text.replace('* ', '• ')
            
            # Membelah keseluruhan teks berdasarkan tag asteris ganda **Teks_Tebal** menggunakan regex
            parts = re.split(r'(\*\*.*?\*\*)', text)
            for part in parts:
                # Memastikan komponen itu bagian blok Teks Tebal (diapit ** pada awalan dan akhiran)
                if part.startswith('**') and part.endswith('**'):
                    # Cetak tanpa tulisan bintang pembungkusnya menggunakan tag 'bold'
                    self.txt_result.insert(tk.END, part[2:-2], 'bold')
                else:
                    # Mencetak bagian teks lainnya secara reguler
                    self.txt_result.insert(tk.END, part, 'normal')
            
            # Memberikan enter (baris baru)
            self.txt_result.insert(tk.END, "\n")
            
        # Perintah ini memaksa scroll bar untuk terus turun ke paling bawah secara otomatis usai teks ditambahkan
        self.txt_result.see(tk.END)
        # Kunci kembali TextBox sebagai Read-Only setelah diproses
        self.txt_result.config(state=tk.DISABLED)

    # Method Triggering - Dimulai saat tombol 'Mulai Analisis' ditekan/diklik
    def start_analysis(self):
        # Pengaman tambahan: Jika belum memilih gambar (nilai self.image_path nol), jangan proses apapun
        if not self.image_path: return
        
        # Ubah kursor dan kondisi agar user tidak dobel-klik saat program sedang berpikir
        self.btn_analyze.config(state=tk.DISABLED)
        self.lbl_loading.config(text="Memproses gambar... mohon tunggu.")
        
        # Konsep OOP: Komposisi Kelas
        # Aplikasi utama (PenyuluhAIApp) memiliki (has-a) komponen objek AI (PakarBotaniSession).
        # Di tahap ini kita melahirkan objek (instansiasi) sesi AI baru secara utuh yang tidak punya riwayat lama.
        self.ai_session = predictor.PakarBotaniSession()
        
        # Melimpahkan proses komunikasi API dengan model (yang butuh waktu internet) ke pekerja di latar belakang (Thread).
        # Tujuannya agar aplikasi (GUI/Mainloop) tidak seketika nge-hang / freeze (layar putih membeku) selagi menunggu AI.
        threading.Thread(target=self.run_prediction, daemon=True).start()

    # Method (Tugas Background/Thread) untuk menugaskan fungsi di kelas lain
    def run_prediction(self):
        # Konsep OOP: Method Invocation (Memanggil fungsi/perilaku milik objek ai_session).
        result = self.ai_session.predict_disease(self.image_path)
        # Menjadwalkan pengiriman pesan output ke method "update_gui_after_prediction" di Thread GUI utama.
        self.root.after(0, self.update_gui_after_prediction, result)

    # Method sinkronisasi GUI: Dipanggil ketika Thread selesai dan mendapatkan jawaban hasil prediksi (result)
    def update_gui_after_prediction(self, result):
        # Matikan indikator label loading "Memproses..."
        self.lbl_loading.config(text="")
        
        # Mendaftarkan histori baru ke listbox UI dan sistem dictionary berdasarkan Timestamp (jam-menit-detik)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.current_session_key = f"Analisis: {current_time}"
        self.history_listbox.insert(tk.END, self.current_session_key)
        
        # Kirim hasil balasan tersebut agar dirender ke TextBox raksasa Obrolan Diskusi
        self.insert_chat_text("AI", result)
        
        # Hidupkan semua kunci kontrol agar pengguna bisa melanjutkan ke tahap menanya (Follow-up)
        self.btn_analyze.config(state=tk.NORMAL)
        self.btn_export.config(state=tk.NORMAL)
        self.btn_send.config(state=tk.NORMAL)
        self.entry_chat.config(state=tk.NORMAL)

    # Method Triggering - Dimulai saat tombol 'Tanya' atau Enter ditekan
    def send_chat(self):
        # Menghapus seluruh spasi berlebih pada awal/akhir kotak ketik 
        question = self.entry_chat.get().strip()
        # Batalkan jika pertanyaannya string kosong, ATAU proses analisis belum pernah diinisiasi (objek AI kosong)
        if not question or not self.ai_session: return
        
        # Hapus sisa kata-kata yang menempel di dalam kolom ketikan
        self.entry_chat.delete(0, tk.END)
        # Cetak pertanyaan itu sendiri ke ruang obrolan GUI atas nama "User"
        self.insert_chat_text("User", question)
        
        # Non-aktifkan tombol kirim sementara menghindari duplikasi spam internet ganda
        self.btn_send.config(state=tk.DISABLED)
        # Tampilkan notifikasi progres 
        self.lbl_loading.config(text="AI sedang mengetik...")
        
        # Eksekusi proses pengiriman HTTP API ke background via Thread (Asynchronous logic)
        threading.Thread(target=self.run_chat, args=(question,), daemon=True).start()

    # Method Background 
    def run_chat(self, question):
        # Konsep OOP: Memanggil fungsi/behavior lanjutan 'ask_follow_up' khusus dari instance objek AI
        result = self.ai_session.ask_follow_up(question)
        # Sinkronkan kembali GUI ketika hasil telah di-generate oleh Google AI
        self.root.after(0, self.update_gui_after_chat, result)

    # Method sinkronisasi obrolan
    def update_gui_after_chat(self, result):
        # Hilangkan tulisan "AI sedang mengetik"
        self.lbl_loading.config(text="")
        # Cetak jawabannya ke layar obrolan
        self.insert_chat_text("AI", result)
        # Bebaskan kunci pengiriman agar orang bisa merespons balik lagi
        self.btn_send.config(state=tk.NORMAL)

    # Method utilitas untuk fungsi "Simpan Laporan"
    def export_report(self):
        # Mengambil absolut semua nilai teks dari baris 1 kolom 0, sampai indikator END
        full_text = self.txt_result.get(1.0, tk.END)
        
        # Membuka pop-up jendela khusus fungsi "Save As" file yang dikhususkan pada ekstensi *.txt
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="Laporan_PenyuluhAI.txt", title="Simpan Laporan")
        
        # Mengecek jika pengguna tidak batal menekan tombol Cancel / X
        if filepath:
            # Membuka file di target path dengan hak Write ("w")
            with open(filepath, "w", encoding="utf-8") as f:
                # Menulis secara utuh semua output mentah ke notepad
                f.write(full_text)
            
            # Tampilkan pesan sistem bahwa file selesai dibuat dan operasi sukses sempurna!
            messagebox.showinfo("Sukses", "Laporan berhasil disimpan!")

# Entry point aplikasi (Main program/Fungsi awal mula yang dieksekusi Sistem Operasi)
if __name__ == "__main__":
    # Konsep OOP: Instansiasi library objek Tcl/Tk root utama ke dalam variabel
    root = tk.Tk()
    
    # Konsep OOP: Instansiasi objek class utama PenyuluhAIApp dan meneruskan window root ke sana (Dependency Injection)
    app = PenyuluhAIApp(root)
    
    # Memerintahkan objek root (window aplikasi) untuk "terkunci" atau selalu loop berulang-ulang tanpa henti,
    # Event-Driven Architecture (listener) - Sistem akan menunggu sambil 'mendengar' pergerakan kursor atau input orang
    root.mainloop()
