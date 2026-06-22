# 🌿 Penyuluh-AI

**Penyuluh-AI** adalah aplikasi desktop cerdas berbasis Python yang berfungsi sebagai asisten dan pakar botani interaktif. Dengan memanfaatkan **Google Gemini 2.5 Flash**, aplikasi ini mampu mengidentifikasi spesies tanaman, mendeteksi penyakit atau kekurangan nutrisi dari foto daun, dan memberikan saran penanganan langsung layaknya seorang ahli.

## 🌟 Fitur Utama
- **Identifikasi Cerdas:** Deteksi jenis tanaman dan penyakit secara spesifik melalui gambar.
- **Kamera Terintegrasi:** Dukungan webcam untuk mengambil foto langsung dari aplikasi.
- **Sesi Tanya-Jawab (Chat):** Pengguna dapat berinteraksi langsung (tanya-jawab) dengan AI tentang hasil diagnosis.
- **Ekspor Laporan:** Simpan seluruh riwayat konsultasi ke dalam file `.txt`.

---

## 💻 Prasyarat
Sebelum menginstal aplikasi ini, pastikan komputer Anda sudah terpasang:
1. **Python 3.8+** (beserta `pip`).
2. *(Khusus Linux/Ubuntu)* Paket `python3-tk` untuk menjalankan GUI: `sudo apt install python3-tk`.
3. **API Key Gemini:** Anda memerlukan API Key gratis dari [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🚀 Cara Instalasi & Menjalankan Aplikasi

Ikuti langkah-langkah di bawah ini secara berurutan menggunakan terminal (misalnya di VS Code):

### 1. Clone Repository
Pertama, unduh kode proyek ini ke komputer Anda:
```bash
git clone https://github.com/USERNAME_ANDA/penyuluh-ai.git
cd penyuluh-ai
```
*(Catatan: Ganti URL di atas dengan link repositori GitHub Anda)*

### 2. Buat Virtual Environment (Opsional tapi Disarankan)
Agar pustaka proyek ini tidak bercampur dengan proyek Python Anda yang lain:
```bash
python3 -m venv venv

# Aktifkan Virtual Environment:
# Untuk Windows:
venv\Scripts\activate
# Untuk Linux / Mac:
source venv/bin/activate
```

### 3. Install Dependensi (Library)
Instal semua pustaka yang dibutuhkan menggunakan `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi API Key
Buka file `predictor.py` di dalam VS Code Anda. 
Cari baris berikut:
```python
API_KEY = "PASTE_API_KEY_ANDA_DI_SINI"
```
Ganti tulisan `PASTE_API_KEY_ANDA_DI_SINI` dengan kunci API Gemini asli Anda yang didapatkan dari Google AI Studio. **Jangan mengunggah (commit) API Key asli Anda ke GitHub terbuka (public)!**

### 5. Jalankan Aplikasi!
Setelah semuanya siap, jalankan perintah ini di terminal:
```bash
python3 main.py
```
Aplikasi GUI Penyuluh-AI akan terbuka dan siap membantu Anda!

---

## 🛠️ Tentang `usbipd` (Bagi Pengguna WSL Windows)
Jika Anda menggunakan Linux virtual melalui WSL pada Windows, tombol "Buka Kamera" mungkin akan ditolak aksesnya oleh sistem. Untuk mengaktifkannya, Anda harus melakukan *bind* kamera dari host Windows menggunakan PowerShell Administrator:
1. `usbipd list`
2. `usbipd bind --busid <ANGKA_BUSID> --force`
3. `usbipd attach --wsl --busid <ANGKA_BUSID>`
4. Lalu beri izin pada WSL: `sudo chmod 777 /dev/video*`

---

*Dibuat untuk memajukan teknologi agrikultur Indonesia.* 🌱
