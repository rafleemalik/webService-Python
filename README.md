# Web Service dengan Python - Laporan Analisis

## 1. Inisialisasi Flask & Database
![Inisialisasi Flask & Database](https://github.com/user-attachments/assets/a046bcd9-c586-4eab-b142-0f7a0fd035e0)

### Penjelasan:
- `Flask(__name__)` → Membuat instance Flask.
- `app.secret_key` → Digunakan untuk menyimpan sesi pengguna.
- `SQLALCHEMY_DATABASE_URI` → Menggunakan database SQLite (`students.db`).
- `SQLAlchemy(app)` → Menghubungkan aplikasi dengan database.
- `HTTPBasicAuth()` → Digunakan untuk autentikasi berbasis username dan password.

---

## 2. Model User (Untuk Otentikasi)
![Model User](https://github.com/user-attachments/assets/90fcb676-4e9c-44d4-a74c-a87b30b0e831)

### Penjelasan:
- Model `User` menyimpan data `username` & `password`.
- `set_password(password)` → Menyimpan password dalam bentuk **hashed**.
- `check_password(password)` → Mengecek apakah password sesuai.

---

## 3. Model Student (Data Mahasiswa)
![Model Student](https://github.com/user-attachments/assets/ee6eada1-9717-4dbf-876d-0035e31d2a8c)

### Penjelasan:
Model `Student` menyimpan informasi berikut:
- `name` → Nama mahasiswa.
- `age` → Umur mahasiswa.
- `grade` → Nilai/Kelas mahasiswa.

---

## 4. Otentikasi Pengguna
![Otentikasi](https://github.com/user-attachments/assets/bfe055be-9462-461f-b0b6-7cb67591f111)

### Penjelasan:
- Mencari **user** berdasarkan `username`.
- Jika ditemukan, **verifikasi password** menggunakan hashing.
- Jika `username` & `password` cocok, user dianggap **terautentikasi**.

---

## 5. Manajemen Login & Logout

### **Login (POST Request)**
![Login](https://github.com/user-attachments/assets/b90bb08d-e92e-449d-aa7d-1745d0a93690)

#### Proses:
1. Mencari user berdasarkan **username**.
2. Mengecek password dengan `check_password()`.
3. Jika benar, menyimpan **user ke dalam session**.
4. Redirect ke halaman daftar mahasiswa (`/students`).
5. Jika login gagal, tampilkan pesan **error**.

### **Logout**
![Logout](https://github.com/user-attachments/assets/09586112-b45c-4c40-a395-4d8990de445c)

#### Proses:
- **Membersihkan sesi pengguna**.
- Redirect ke halaman utama (`index`).

---

## 6. CRUD Data Mahasiswa

### **Read (Menampilkan Daftar Mahasiswa)**
![Read](https://github.com/user-attachments/assets/91a80730-99a9-4869-9a6e-fe413c12af26)

#### Penjelasan:
- Hanya bisa diakses jika **user sudah login**.
- Mengambil semua data mahasiswa (`Student.query.all()`).
- Menampilkan daftar mahasiswa.

### **Create (Menambahkan Mahasiswa Baru)**
![Create](https://github.com/user-attachments/assets/2bd2c16b-b9fb-4226-904b-63937f2cedf7)

#### Penjelasan:
- **User harus login**.
- Data mahasiswa diambil dari **form** dan disimpan ke database.

### **Update (Edit Mahasiswa)**
![Update](https://github.com/user-attachments/assets/81fa2380-6038-45ed-a3b0-3873efa7f24a)

#### Penjelasan:
- **User harus login**.
- Mengambil mahasiswa berdasarkan `id`.
- Jika `POST`, data mahasiswa diperbarui.

### **Delete (Menghapus Data Mahasiswa)**
![Delete](https://github.com/user-attachments/assets/02728b98-86fb-44b9-8de7-8b6ef146a670)

#### Penjelasan:
- **User harus login**.
- Mahasiswa ditemukan berdasarkan `id`, lalu dihapus dari database.

---

## 7. Pembuatan User Baru
![Create User](https://github.com/user-attachments/assets/7d9070a9-8275-4b1d-b83b-40a829e80067)

### Penjelasan:
- Fitur **Create User** memungkinkan pengguna **mendaftar dengan username dan password**.
- Password di-**hash** menggunakan `generate_password_hash()` sebelum disimpan.
- Sistem memeriksa **duplikasi username** dan memastikan input **tidak kosong**.
- Jika valid, **user baru disimpan ke database** menggunakan SQLAlchemy.
- **Verifikasi login** dilakukan dengan `check_password_hash()`.

---

## 8. Class Diagram
![Class Diagram](https://github.com/user-attachments/assets/b34329da-0032-43c7-b64b-53e8769ce46b)

Diagram ini menunjukkan bagaimana aplikasi Flask mengelola **data pengguna dan mahasiswa**. FlaskApp adalah inti aplikasi yang menggunakan **SQLAlchemy** untuk database dan **HTTPBasicAuth** untuk autentikasi.

**Model Utama:**
- `User` → Menyimpan data pengguna (`username`, `password_hash`) serta memiliki fungsi **set dan check password**.
- `Student` → Menyimpan informasi mahasiswa seperti **nama, umur, dan nilai**.
- `FlaskApp` → Terhubung dengan `User` untuk **login/logout**, dan dengan `Student` untuk **mengelola data mahasiswa**.

---

## 9. Use Case Diagram
![Use Case Diagram](https://github.com/user-attachments/assets/34b12cf9-4ad0-4ec6-8f29-4335da80e480)

Diagram ini menunjukkan **alur kerja aplikasi** dalam mengelola data **pengguna dan mahasiswa**.

### **Peran Utama:**
- **User** → Bisa **login, logout, melihat daftar mahasiswa**, serta **menambah, mengedit, menghapus data mahasiswa, dan pembuatan pengguna baru**.
- **Admin** → Memiliki **kontrol lebih luas**, termasuk **pembuatan pengguna baru**.

---

## 10. Sequence Diagram
![Sequence Diagram](https://github.com/user-attachments/assets/3d13591d-bb66-42f6-b3a8-ddcdd592243b)

### Penjelasan:
- **User/Admin** bisa **login, menambah, mengedit, melihat, dan menghapus data mahasiswa**.
- Setiap aksi diproses oleh **FlaskApp**, diteruskan ke **Authentication Logic & CRUD**, lalu berinteraksi dengan **database**.
- Contoh:
  - Saat **menambah mahasiswa**, sistem akan **menyimpan data baru ke database**.
  - Saat **mengedit/hapus mahasiswa**, sistem akan **mencari data sebelum diubah/dihapus**.
- **Logout** akan menghapus **sesi pengguna** dari sistem.

