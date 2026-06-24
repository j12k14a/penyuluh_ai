import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk # Library Pillow untuk mengolah dan menampilkan gambar
import threading # Untuk menjalankan proses AI di thread terpisah
import re # Regular Expression untuk memformat output AI
import cv2 # OpenCV untuk akses kamera
import predictor # File predictor.py yang berisi logika AI

# Tema Warna Agrikultur yang elegan
BG_COLOR = "#F1F8E9"         
PRIMARY_COLOR = "#2E7D32"    
SECONDARY_COLOR = "#A5D6A7"  
TEXT_COLOR = "#1B5E20"       
FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_NORMAL = ("Segoe UI", 12)
FONT_RESULT = ("Segoe UI", 12)

class PenyuluhAIApp:
    # Constructor
    # Dipanggil otomatis saat object dibuat
    def __init__(self, root):
        self.root = root # Menyimpan window utama Tkinter ke dalam object, self merepresentasikan object yang sedang aktif
        self.root.title("Penyuluh-AI: Sistem Pakar Botani Interaktif")
        self.root.geometry("1000x900")
        self.root.configure(bg=BG_COLOR)
        
        self.image_path = None # Menyimpan lokasi gambar yang dipilih user
        self.ai_session = None  # Objek memori percakapan
        
        self.create_widgets() # Membuat seluruh komponen GUI
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=PRIMARY_COLOR, pady=15) # Membuat container/frame untuk bagian header aplikasi
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="🌿 Penyuluh-AI", font=FONT_TITLE, bg=PRIMARY_COLOR, fg="white")
        title_label.pack()
        
        # Area Tombol Utama btn = button
        btn_frame = tk.Frame(self.root, bg=BG_COLOR, pady=10)
        btn_frame.pack()

        self.btn_select = tk.Button(btn_frame, text="📁 Pilih Foto", font=("Segoe UI", 11, "bold"), bg=SECONDARY_COLOR, command=self.select_image)
        self.btn_select.grid(row=0, column=0, padx=10)

        self.btn_camera = tk.Button(btn_frame, text="📸 Buka Kamera", font=("Segoe UI", 11, "bold"), bg=SECONDARY_COLOR, command=self.open_camera)
        self.btn_camera.grid(row=0, column=1, padx=10)

        self.btn_analyze = tk.Button(btn_frame, text="🔍 Mulai Analisis", font=("Segoe UI", 11, "bold"), bg=PRIMARY_COLOR, fg="white", command=self.start_analysis, state=tk.DISABLED)
        self.btn_analyze.grid(row=0, column=2, padx=10)

        self.btn_export = tk.Button(btn_frame, text="💾 Simpan Laporan", font=("Segoe UI", 11, "bold"), bg="#FFB300", command=self.export_report, state=tk.DISABLED)
        self.btn_export.grid(row=0, column=3, padx=10)

        # Content Area
        content_frame = tk.Frame(self.root, bg=BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Kolom Kiri: Gambar
        left_frame = tk.Frame(content_frame, bg=BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.image_label = tk.Label(left_frame, bg="#C8E6C9", text="Pratinjau Gambar", font=FONT_NORMAL, width=40, height=15)
        self.image_label.pack(pady=10)
        
        self.lbl_loading = tk.Label(left_frame, text="", font=("Segoe UI", 11, "italic"), bg=BG_COLOR, fg=PRIMARY_COLOR)
        self.lbl_loading.pack()

        # Kolom Kanan: Hasil & Chat
        right_frame = tk.Frame(content_frame, bg=BG_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20,0))
        
        # Text Box Chat
        self.txt_result = tk.Text(right_frame, font=FONT_RESULT, wrap=tk.WORD, bg="white", height=20, width=50)
        self.txt_result.pack(fill=tk.BOTH, expand=True)
        self.txt_result.tag_configure('bold', font=("Segoe UI", 12, "bold"), foreground=PRIMARY_COLOR)
        self.txt_result.tag_configure('normal', font=FONT_RESULT)
        self.txt_result.tag_configure('user', font=("Segoe UI", 12, "italic"), foreground="blue", justify='right')
        
        # Scrollbar untuk text box
        scrollbar = tk.Scrollbar(self.txt_result)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_result.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.txt_result.yview)

        # Input Chat Lanjutan
        chat_input_frame = tk.Frame(right_frame, bg=BG_COLOR, pady=10)
        chat_input_frame.pack(fill=tk.X)
        
        self.entry_chat = tk.Entry(chat_input_frame, font=FONT_NORMAL)
        self.entry_chat.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.entry_chat.bind("<Return>", lambda event: self.send_chat())
        
        self.btn_send = tk.Button(chat_input_frame, text="Tanya", bg=PRIMARY_COLOR, fg="white", font=("Segoe UI", 10, "bold"), command=self.send_chat, state=tk.DISABLED)
        self.btn_send.pack(side=tk.RIGHT, padx=5)

    def select_image(self):
        filepath = filedialog.askopenfilename(filetypes=[('Gambar', '*.png *.jpg *.jpeg *.bmp')])
        if filepath:
            self.image_path = filepath
            self.display_image(filepath)
            self.btn_analyze.config(state=tk.NORMAL)
            self.clear_chat()
            self.insert_chat_text("Sistem", "Foto dimuat dari galeri. Klik 'Mulai Analisis'!")

    def open_camera(self):
        # Membuka kamera dengan OpenCV = Method
        cap = cv2.VideoCapture(0) # Mengaktifkan webcam default komputer
        if not cap.isOpened(): # Mengecek apakah kamera berhasil dibuka
            messagebox.showerror("Error Kamera", "Kamera tidak ditemukan atau ditolak aksesnya oleh sistem operasi (Sering terjadi di WSL Linux).")
            return
            
        # Pemanasan sensor kamera (Linux butuh waktu untuk membuka lensa)
        import time
        for _ in range(15):
            cap.read()
            time.sleep(0.05)
            
        ret, frame = cap.read()
        if ret:
            # Simpan foto sementara
            temp_path = "temp_camera.jpg"
            cv2.imwrite(temp_path, frame) # Mengambil satu frame gambar dari kamera.
            self.image_path = temp_path   # Menyimpan lokasi gambar.
            self.display_image(temp_path) # Menampilkan gambar ke GUI.
            self.btn_analyze.config(state=tk.NORMAL)
            self.clear_chat()
            self.insert_chat_text("Sistem", "Foto berhasil diambil dari kamera. Klik 'Mulai Analisis'!")
        else:
            messagebox.showerror("Error", "Gagal menangkap gambar dari kamera.")
        
        cap.release()

    def display_image(self, path): 
        try:
            img = Image.open(path)
            img.thumbnail((450, 450), Image.Resampling.LANCZOS) # Mengecilkan gambar agar sesuai area GUI;Mengubah gambar Pillow menjadi format yang dapat ditampilkan Tkinter.
            photo = ImageTk.PhotoImage(img) 
            self.image_label.config(image=photo, text="", width=450, height=450)
            self.image_label.image = photo
        except Exception as e:
            pass

    def clear_chat(self):
        self.txt_result.config(state=tk.NORMAL)
        self.txt_result.delete(1.0, tk.END)
        self.txt_result.config(state=tk.DISABLED)

    def insert_chat_text(self, sender, text):
        self.txt_result.config(state=tk.NORMAL)
        
        if sender == "User":
            self.txt_result.insert(tk.END, f"\nAnda:\n{text}\n\n", 'user')
        elif sender == "Sistem":
            self.txt_result.insert(tk.END, f"\n[INFO] {text}\n", 'normal')
        else: # AI
            self.txt_result.insert(tk.END, f"\n--- Pakar Botani ---\n", 'bold')
            text = text.replace('* ', '• ')
            parts = re.split(r'(\*\*.*?\*\*)', text)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    self.txt_result.insert(tk.END, part[2:-2], 'bold')
                else:
                    self.txt_result.insert(tk.END, part, 'normal')
            self.txt_result.insert(tk.END, "\n")
            
        self.txt_result.see(tk.END)
        self.txt_result.config(state=tk.DISABLED)

    def start_analysis(self):
        if not self.image_path: return
        self.btn_analyze.config(state=tk.DISABLED) # Tombol dinonaktifkan terlebih dahulu sampai user memilih gambar.
        self.lbl_loading.config(text="Memproses gambar... mohon tunggu.")
        
        # Buat sesi AI baru
        self.ai_session = predictor.PakarBotaniSession()
        # Menjalankan analisis AI di thread terpisah agar GUI tidak freeze.
        threading.Thread(target=self.run_prediction, daemon=True).start() 

    def run_prediction(self):
        result = self.ai_session.predict_disease(self.image_path) # Mengirim gambar ke Gemini AI untuk dianalisis.
        self.root.after(0, self.update_gui_after_prediction, result)

    def update_gui_after_prediction(self, result):
        self.lbl_loading.config(text="")
        self.insert_chat_text("AI", result)
        self.btn_analyze.config(state=tk.NORMAL)
        self.btn_export.config(state=tk.NORMAL)
        self.btn_send.config(state=tk.NORMAL)

    def send_chat(self):
        question = self.entry_chat.get().strip() # Mengambil pertanyaan dari user.
        if not question or not self.ai_session: return
        
        self.entry_chat.delete(0, tk.END)
        self.insert_chat_text("User", question)
        self.btn_send.config(state=tk.DISABLED)
        self.lbl_loading.config(text="AI sedang mengetik...")
        
        threading.Thread(target=self.run_chat, args=(question,), daemon=True).start()

    def run_chat(self, question):
        result = self.ai_session.ask_follow_up(question) # Mengirim pertanyaan lanjutan ke AI.
        self.root.after(0, self.update_gui_after_chat, result)

    def update_gui_after_chat(self, result):
        self.lbl_loading.config(text="")
        self.insert_chat_text("AI", result)
        self.btn_send.config(state=tk.NORMAL)

    def export_report(self):
        # Ambil semua teks dari text box
        full_text = self.txt_result.get(1.0, tk.END)
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="Laporan_PenyuluhAI.txt", title="Simpan Laporan")
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f: # Membuat file laporan baru.
                f.write(full_text) # Menyimpan hasil percakapan ke file.
            messagebox.showinfo("Sukses", "Laporan berhasil disimpan!")
            
# Mengecek apakah file ini dijalankan langsung oleh Python
# Jika iya, maka nilai __name__ akan menjadi "__main__"
# Jika file ini hanya di-import oleh file lain, blok ini tidak akan dijalankan
if __name__ == "__main__":

    # Membuat window utama (root window) dari Tkinter
    # Semua komponen GUI akan ditempatkan di dalam window ini
    root = tk.Tk()

    # Membuat object dari class PenyuluhAIApp
    # Constructor (__init__) akan dipanggil otomatis
    # dan seluruh tampilan aplikasi akan dibuat
    app = PenyuluhAIApp(root)

    # Menjalankan event loop Tkinter
    # Program akan terus berjalan dan menunggu interaksi user
    # seperti klik tombol, input keyboard, atau event lainnya
    root.mainloop()
