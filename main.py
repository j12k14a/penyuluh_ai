import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import threading
import re
import cv2
import predictor
import os
import json

# Import modul datetime untuk mencatat waktu histori
import datetime

# Tema Warna Agrikultur yang elegan
BG_COLOR = "#F1F8E9"         
PRIMARY_COLOR = "#2E7D32"    
SECONDARY_COLOR = "#A5D6A7"  
TEXT_COLOR = "#1B5E20"       
FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_NORMAL = ("Segoe UI", 12)
FONT_RESULT = ("Segoe UI", 12)

class PenyuluhAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Penyuluh-AI: Sistem Pakar Botani Interaktif")
        self.root.geometry("1000x900")
        self.root.configure(bg=BG_COLOR)
        
        self.image_path = None
        self.ai_session = None  # Objek memori percakapan
        self.current_session_key = None
        self.history_data = {}
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header (digabung dengan kolom kiri)
        # Area Tombol Utama (digabung dengan kolom kiri)
        # Content Area
        # Mengubah struktur frame utama untuk menampung 3 kolom
        content_frame = tk.Frame(self.root, bg=BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Kolom Kiri: Gambar dan Header
        # Menambahkan frame kiri dengan warna latar hijau muda dan lebar tetap
        left_frame = tk.Frame(content_frame, bg=SECONDARY_COLOR, width=280)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left_frame.pack_propagate(False)

        # Memindahkan judul aplikasi ke kolom kiri
        title_label = tk.Label(left_frame, text="🌿 Penyuluh-AI", font=("Segoe UI", 20, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR)
        title_label.pack(pady=20)
        
        self.image_label = tk.Label(left_frame, bg="white", text="Pratinjau Gambar", font=FONT_NORMAL, width=30, height=12)
        self.image_label.pack(pady=10, padx=10)
        
        # Memindahkan tombol-tombol ke bawah gambar di kolom kiri
        self.btn_select = tk.Button(left_frame, text="📁 Pilih Foto", font=("Segoe UI", 11, "bold"), bg=PRIMARY_COLOR, fg="white", command=self.select_image)
        self.btn_select.pack(fill=tk.X, padx=20, pady=5)

        self.btn_camera = tk.Button(left_frame, text="📸 Buka Kamera", font=("Segoe UI", 11, "bold"), bg=PRIMARY_COLOR, fg="white", command=self.open_camera)
        self.btn_camera.pack(fill=tk.X, padx=20, pady=5)

        self.btn_analyze = tk.Button(left_frame, text="🔍 Mulai Analisis", font=("Segoe UI", 11, "bold"), bg="#FFB300", fg="black", command=self.start_analysis, state=tk.DISABLED)
        self.btn_analyze.pack(fill=tk.X, padx=20, pady=15)
        
        self.lbl_loading = tk.Label(left_frame, text="", font=("Segoe UI", 11, "italic"), bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        self.lbl_loading.pack()

        # Spacer agar elemen di bawah terdorong ke paling bawah kolom kiri
        spacer = tk.Frame(left_frame, bg=SECONDARY_COLOR)
        spacer.pack(fill=tk.BOTH, expand=True)

        try:
            if os.path.exists("logo_app.png"):
                logo_pil = Image.open("logo_app.png")
                self.logo_img = ImageTk.PhotoImage(logo_pil)
                self.lbl_logo = tk.Label(left_frame, image=self.logo_img, bg=SECONDARY_COLOR)
                self.lbl_logo.pack(side=tk.BOTTOM, pady=(0, 20))
        except Exception:
            pass

        self.lbl_watermark = tk.Label(left_frame, text="Builder by Kelompok 6 PBO", font=("Segoe UI", 10, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR)
        self.lbl_watermark.pack(side=tk.BOTTOM, pady=(10, 5))

        # Kolom Tengah: Chat
        # Membuat frame tengah untuk ruang diskusi
        middle_frame = tk.Frame(content_frame, bg=BG_COLOR)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Menambahkan judul untuk ruang diskusi
        middle_title = tk.Label(middle_frame, text="Ruang Diskusi & Hasil", font=("Segoe UI", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        middle_title.pack(pady=10)

        # Text Box Chat
        self.txt_result = tk.Text(middle_frame, font=FONT_RESULT, wrap=tk.WORD, bg="white")
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
        chat_input_frame = tk.Frame(middle_frame, bg=BG_COLOR, pady=10)
        chat_input_frame.pack(fill=tk.X)
        
        self.entry_chat = tk.Entry(chat_input_frame, font=FONT_NORMAL)
        self.entry_chat.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.entry_chat.bind("<Return>", lambda event: self.send_chat())
        
        self.btn_send = tk.Button(chat_input_frame, text="Tanya", bg=PRIMARY_COLOR, fg="white", font=("Segoe UI", 10, "bold"), command=self.send_chat, state=tk.DISABLED)
        self.btn_send.pack(side=tk.RIGHT, padx=5)

        # Kolom Kanan: Hasil & Chat (Disesuaikan menjadi Menu Lanjutan dan Histori)
        # Menambahkan frame kanan untuk menu lanjutan dan histori penyuluhan
        right_frame = tk.Frame(content_frame, bg=SECONDARY_COLOR, width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        right_frame.pack_propagate(False)
        
        # Menambahkan judul Menu Lanjutan
        right_title = tk.Label(right_frame, text="Menu Lanjutan", font=("Segoe UI", 14, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR)
        right_title.pack(pady=20)
        
        self.btn_export = tk.Button(right_frame, text="💾 Simpan Laporan", font=("Segoe UI", 11, "bold"), bg="#E64A19", fg="white", command=self.export_report, state=tk.DISABLED)
        self.btn_export.pack(fill=tk.X, padx=20, pady=10)
        
        # Menambahkan judul dan listbox untuk histori chat
        history_title = tk.Label(right_frame, text="Histori Penyuluhan", font=("Segoe UI", 12, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR)
        history_title.pack(pady=(20, 5))
        
        self.history_listbox = tk.Listbox(right_frame, font=FONT_NORMAL)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Menambahkan scrollbar untuk listbox histori
        hist_scrollbar = tk.Scrollbar(self.history_listbox)
        hist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=hist_scrollbar.set)
        hist_scrollbar.config(command=self.history_listbox.yview)
        
        # Memuat riwayat dari file (jika ada) saat aplikasi dimulai
        self.load_history()
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)

    def load_history(self):
        # Membaca file histori dan memasukkannya ke dalam listbox
        if os.path.exists("history_data.json"):
            try:
                with open("history_data.json", "r", encoding="utf-8") as f:
                    self.history_data = json.load(f)
                for key in self.history_data:
                    self.history_listbox.insert(tk.END, key)
            except Exception as e:
                pass

    def save_history_data(self):
        # Menyimpan seluruh data histori ke file JSON
        with open("history_data.json", "w", encoding="utf-8") as f:
            json.dump(self.history_data, f, indent=4)

    def on_history_select(self, event):
        # Callback saat item histori di klik
        selection = self.history_listbox.curselection()
        if not selection: return
        idx = selection[0]
        session_key = self.history_listbox.get(idx)
        
        if session_key in self.history_data:
            self.current_session_key = session_key
            self.clear_chat()
            # Memuat ulang riwayat chat ke layar
            for msg in self.history_data[session_key]:
                self.insert_chat_text(msg["sender"], msg["text"], save=False)
            
            # Nonaktifkan sementara dan muat ulang memori AI di background
            self.btn_send.config(state=tk.DISABLED)
            self.entry_chat.config(state=tk.DISABLED)
            self.lbl_loading.config(text="Memuat ulang memori percakapan...")
            
            import threading
            threading.Thread(target=self.reconstruct_session, args=(self.history_data[session_key],), daemon=True).start()

    def reconstruct_session(self, history_list):
        self.ai_session = predictor.PakarBotaniSession(history_data=history_list)
        self.root.after(0, self.update_gui_after_reconstruct)
        
    def update_gui_after_reconstruct(self):
        self.lbl_loading.config(text="")
        self.btn_send.config(state=tk.NORMAL)
        self.entry_chat.config(state=tk.NORMAL)
        self.btn_export.config(state=tk.NORMAL)

    def select_image(self):
        filepath = filedialog.askopenfilename(filetypes=[('Gambar', '*.png *.jpg *.jpeg *.bmp')])
        if filepath:
            self.image_path = filepath
            self.display_image(filepath)
            self.btn_analyze.config(state=tk.NORMAL)
            self.current_session_key = None
            self.clear_chat()
            self.insert_chat_text("Sistem", "Foto dimuat dari galeri. Klik 'Mulai Analisis'!")

    def open_camera(self):
        # Membuka kamera dengan OpenCV
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
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
            cv2.imwrite(temp_path, frame)
            self.image_path = temp_path
            self.display_image(temp_path)
            self.btn_analyze.config(state=tk.NORMAL)
            self.current_session_key = None
            self.clear_chat()
            self.insert_chat_text("Sistem", "Foto berhasil diambil dari kamera. Klik 'Mulai Analisis'!")
        else:
            messagebox.showerror("Error", "Gagal menangkap gambar dari kamera.")
        
        cap.release()

    def display_image(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((450, 450), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo, text="", width=450, height=450)
            self.image_label.image = photo
        except Exception as e:
            pass

    def clear_chat(self):
        self.txt_result.config(state=tk.NORMAL)
        self.txt_result.delete(1.0, tk.END)
        self.txt_result.config(state=tk.DISABLED)

    def insert_chat_text(self, sender, text, save=True):
        self.txt_result.config(state=tk.NORMAL)
        
        # Simpan pesan ke memori histori jika mode simpan aktif
        if save and self.current_session_key:
            if self.current_session_key not in self.history_data:
                self.history_data[self.current_session_key] = []
            self.history_data[self.current_session_key].append({"sender": sender, "text": text})
            self.save_history_data()
        
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
        self.btn_analyze.config(state=tk.DISABLED)
        self.lbl_loading.config(text="Memproses gambar... mohon tunggu.")
        
        # Buat sesi AI baru
        self.ai_session = predictor.PakarBotaniSession()
        
        threading.Thread(target=self.run_prediction, daemon=True).start()

    def run_prediction(self):
        result = self.ai_session.predict_disease(self.image_path)
        self.root.after(0, self.update_gui_after_prediction, result)

    def update_gui_after_prediction(self, result):
        self.lbl_loading.config(text="")
        
        # Buat sesi baru dan masukkan ke dalam listbox history
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.current_session_key = f"Analisis: {current_time}"
        self.history_listbox.insert(tk.END, self.current_session_key)
        
        self.insert_chat_text("AI", result)
        self.btn_analyze.config(state=tk.NORMAL)
        self.btn_export.config(state=tk.NORMAL)
        self.btn_send.config(state=tk.NORMAL)
        self.entry_chat.config(state=tk.NORMAL)

    def send_chat(self):
        question = self.entry_chat.get().strip()
        if not question or not self.ai_session: return
        
        self.entry_chat.delete(0, tk.END)
        self.insert_chat_text("User", question)
        self.btn_send.config(state=tk.DISABLED)
        self.lbl_loading.config(text="AI sedang mengetik...")
        
        threading.Thread(target=self.run_chat, args=(question,), daemon=True).start()

    def run_chat(self, question):
        result = self.ai_session.ask_follow_up(question)
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
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_text)
            messagebox.showinfo("Sukses", "Laporan berhasil disimpan!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PenyuluhAIApp(root)
    root.mainloop()
