# 📝 Aplikasi To-Do List (Flask + SQLite)

Aplikasi web sederhana **To-Do List** yang dibuat menggunakan **Flask**, **SQLAlchemy**, dan **SQLite3**.  
Aplikasi ini memungkinkan pengguna untuk membuat, melihat, mengedit, dan menghapus tugas dengan antarmuka web yang simpel.

---

## 📌 Fitur
- Menambahkan tugas baru
- Melihat daftar semua tugas
- Mengedit tugas yang sudah ada
- Menghapus tugas
- Data tersimpan permanen di database SQLite

---

## 📂 Struktur Proyek

todoweb/
│
├── app.py # File utama Flask
├── database.db # File database SQLite3
├── templates/ # Template HTML (Jinja2)
│ ├── index.html
│ └── edit.html
├── static/ # File statis (CSS, JS)
├── requirements.txt # Daftar dependensi Python
└── README.md # Dokumentasi proyek

## Instalasi & Menjalankan

1 Clone repositori ini
```bash
drive.google.com/drive/file/sourcecode

2️⃣ Buat & aktifkan virtual environment (disarankan)
bash
Copy
Edit
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependensi

pip install -r requirements.txt

Jika belum ada requirements.txt, bisa install manual

pip install flask flask_sqlalchemy

4️⃣ Inisialisasi database

Pastikan di app.py terdapat kode:

with app.app_context():
    db.create_all()

Lalu jalankan:

python app.py

File database.db akan otomatis dibuat.


▶️ Menjalankan Aplikasi

python app.py

Buka browser dan kunjungi:

http://127.0.0.1:5000/

🛠️ Mengakses Database SQLite

Untuk membuka database secara manual:

sqlite3 database.db

Di dalam SQLite:

.tables              -- Melihat semua tabel
SELECT * FROM tasks; -- Melihat semua data tugas
.exit                -- Keluar dari SQLite

📜 Lisensi
Proyek ini bersifat open-source dan gratis digunakan.

🙌 Pembuat
Dibuat oleh Lutfhi Alfadhillah

THANKS FOR USED MY WEB AND APPS


