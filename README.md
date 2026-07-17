# 🌿 Penyuluh-AI

<img width="1076" height="965" alt="image" src="https://github.com/user-attachments/assets/8e38fd46-f027-466f-86dc-ac508665cf2b" />

**Penyuluh-AI** adalah aplikasi desktop cerdas berbasis Python yang berfungsi sebagai asisten dan pakar botani interaktif. Dengan memanfaatkan **Google Gemini 2.5 Flash**, aplikasi ini mampu mengidentifikasi spesies tanaman, mendeteksi penyakit atau kekurangan nutrisi dari foto daun, dan memberikan saran penanganan langsung layaknya seorang ahli.

## 🌟 Fitur Utama
- **Identifikasi Cerdas:** Deteksi jenis tanaman dan penyakit secara spesifik melalui gambar.
- **Kamera Terintegrasi:** Dukungan webcam untuk mengambil foto langsung dari aplikasi.
- **Sesi Tanya-Jawab (Chat):** Pengguna dapat berinteraksi langsung (tanya-jawab) dengan AI tentang hasil diagnosis.
- **Ekspor Laporan:** Simpan seluruh riwayat konsultasi ke dalam file `.txt`.

---

## 🚀 Cara Instalasi & Menjalankan Aplikasi (Khusus Windows)

Bagi rekan-rekan yang menggunakan **Windows 10/11**, silakan ikuti panduan instalasi dari nol (Step 0) berikut ini:

### Step 0: Persiapan Sistem
1. Pastikan laptop Anda sudah terinstal **Python 3.8** atau lebih baru. 
   - *Jika belum punya, silakan download dari [python.org/downloads](https://www.python.org/downloads/). Saat awal proses instalasi, **SANGAT PENTING** untuk mencentang kotak bertuliskan `Add Python to PATH` di bagian bawah jendela installer.*
2. Siapkan **API Key Gemini** secara gratis dari [Google AI Studio](https://aistudio.google.com/app/apikey).

### Step 1: Unduh Proyek
Buka aplikasi **Command Prompt (CMD)**, **PowerShell**, atau terminal **VS Code**. Ketik perintah ini:
```cmd
git clone https://github.com/USERNAME_ANDA/penyuluh-ai.git
cd penyuluh-ai
```
*(Jika Anda tidak punya Git, Anda bisa mendownload proyek ini sebagai file `.zip` di GitHub, lalu ekstrak foldernya dan buka CMD di dalam folder tersebut).*

### Step 2: Buat Lingkungan Virtual (Virtual Environment)
Langkah ini sangat disarankan agar library aplikasi ini tidak bertabrakan dengan proyek Python lain di laptop Anda:
```cmd
python -m venv venv
```
Setelah dibuat, **aktifkan** lingkungannya dengan perintah:
```cmd
venv\Scripts\activate
```
*(Tanda bahwa ini berhasil adalah munculnya tulisan `(venv)` di sebelah kiri baris CMD/PowerShell Anda).*

### Step 3: Install Pustaka Tambahan (Library)
Mari kita pasang semua alat yang dibutuhkan aplikasi (OpenCV, AI, dll):
```cmd
pip install -r requirements.txt
```
*(Tunggu proses unduhan hingga selesai dan muncul tulisan 'Successfully installed...').*

### Step 4: Memasang Kunci API
1. Buka folder proyek ini, cari file bernama `predictor.py`, lalu buka menggunakan Code Editor favorit Anda (seperti VS Code atau Notepad).
2. Cari baris berikut (ada di bagian atas file):
   ```python
   API_KEY = "PASTE_API_KEY_ANDA_DI_SINI"
   ```
3. Hapus tulisan `PASTE_API_KEY_ANDA_DI_SINI` dan ganti (Paste) dengan kode rahasia yang Anda dapatkan dari Google AI Studio. 
4. **Save (Simpan)** file tersebut.

### Step 5: Menjalankan Aplikasi
Semua sudah siap! Pastikan terminal Anda masih berada di dalam folder proyek dan `(venv)` masih aktif. Jalankan aplikasi dengan perintah:
```cmd
python main.py
```
Aplikasi GUI Penyuluh-AI akan otomatis terbuka. Jika Anda menekan tombol "Buka Kamera", lampu webcam laptop Windows Anda akan langsung menyala! 🎉

---

## 🐧 Pengguna Linux / MacOS
Bagi yang menggunakan sistem operasi berbasis Unix (Linux/Mac) atau WSL, proses instalasi kurang lebih sama. Perbedaan utamanya hanya pada cara aktivasi environment dan perintah pemanggilannya:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
*(Catatan Khusus WSL: Akses webcam dari WSL memerlukan proses `bind` perangkat USB menggunakan aplikasi `usbipd` di host Windows).*

---
*Dibuat untuk memajukan teknologi agrikultur Indonesia.* 🌱
