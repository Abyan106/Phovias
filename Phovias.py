# ==========================================
# PHOVIAS
# Kelompok 3
# Atsilla Kaysa Asyraf
# Irenia Maisa Kamila
# Muhammad Abyan Daryansyah
# Najahah Patin
# Dzaky Hafidz Naufal
# ==========================================

import pandas as pd
import os

FILE_PATH = "users.csv"

def load_users():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["id", "name", "role", "password"])
        df.to_csv(FILE_PATH, index=False)
    return pd.read_csv(FILE_PATH)

cameras = [
    {"id": 1, "name": "Canon EOS R6", "category": "Mirrorless"},
    {"id": 2, "name": "Sony A6400", "category": "Mirrorless"},
    {"id": 3, "name": "Nikon D3500", "category": "DSLR"},
    {"id": 4, "name": "Fujifilm X100V", "category": "Compact"},
]

# Histori (didefinisikan agar tidak error saat diakses)
rental_history = []
transaction_history = []

# =========================
# USER AUTH FUNCTIONS
# =========================

def register_user():
    df = load_users()

    print("\n=== REGISTRASI AKUN ===")
    print("1. User")
    print("2. Vendor")

    pilihan = input("Daftar sebagai (1/2): ")

    if pilihan == "1":
        role = "user"
    elif pilihan == "2":
        role = "vendor"
    else:
        print("❌ Pilihan tidak valid!")
        return

    name = input("Masukkan nama: ")
    password = input("Masukkan password: ")

    if name in df["name"].values:
        print("❌ Nama sudah terdaftar!\n")
        return

    new_id = df["id"].max() + 1 if not df.empty else 1

    new_user = {
        "id": new_id,
        "name": name,
        "role": role,
        "password": password
    }

    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

    print(f"✅ Registrasi berhasil sebagai {role}! Selamat datang, {name}.\n")




def login_user():
    df = load_users()

    print("\n=== LOGIN ===")
    name = input("Nama: ")
    password = input("Password: ")

    user = df[(df["name"] == name) & (df["password"] == password)]

    if not user.empty:
        u = user.iloc[0]
        print(f"✅ Login berhasil! Halo, {u['name']} ({u['role']})\n")
        return u.to_dict()

    print("❌ Nama atau password salah!\n")
    return None


# =========================
# USER MENU (CAMERA)
# =========================

def user_menu():
    while True:
        print("\n=== MENU USER ===")
        print("1. Cari Kamera")
        print("2. Lihat Kategori Kamera")
        print("3. Lihat Semua Kamera")
        print("4. Logout")

        choice = input("Pilih menu: ")

        if choice == "1":
            search_camera()
        elif choice == "2":
            list_categories()
        elif choice == "3":
            list_all_cameras()
        elif choice == "4":
            print("👋 Keluar dari menu user.\n")
            break
        else:
            print("❌ Pilihan tidak valid!\n")
            
def view_camera_detail(cam, user):
    print(f"""
=== DETAIL PRODUK ===
ID           : {cam['id']}
Nama Produk  : {cam['nama_produk']}
Jenis        : {cam['jenis_produk']}
Kategori     : {cam['kategori']}
Deskripsi    : {cam['deskripsi']}
Harga Sewa   : {cam['harga_sewa']}
Stok         : {cam['stok']}
Kondisi      : {cam['kondisi']}
Status       : {cam['status']}
-------------------------
""")

    if cam["status"] != "tersedia" or int(cam["stok"]) <= 0:
        print("Produk tidak tersedia untuk disewa.")
        return

    pilih = input("Mau sewa produk ini? (y/n): ").lower()

    if pilih == "y":
        ajukan_sewa(cam, user)
        print("Proposal telah di kirim ke vendor\n")
    elif pilih == "n":
        print("Kembali ke menu.\n")        
    else:
        print("Pilihan tidak valid!!\n")

def pilih_dan_baca_produk(df, user):
    if df.empty:
        print("Tidak ada produk.")
        return

    for _, row in df.iterrows():
        print(f"- ID {row['id']} | {row['nama_produk']} ({row['kategori']})")

    cid = input("Masukkan ID produk (atau kosong untuk batal): ")

    if not cid.isdigit():
        print("Batal.")
        return

    cid = int(cid)
    cam = df[df["id"] == cid]

    if cam.empty:
        print("Produk tidak ditemukan.")
        return

    view_camera_detail(cam.iloc[0], user)


def search_camera():
    key = input("Masukkan nama kamera: ").lower()
    print("\n=== HASIL PENCARIAN ===")
    found = False

    for cam in cameras:
        if key in cam["name"].lower():
            print(f"- ID {cam['id']} | {cam['name']} ({cam['category']})")
            found = True

    if not found:
        print("❌ Kamera tidak ditemukan.")


def list_categories():
    categories = sorted(list(set(cam["category"] for cam in cameras)))

    print("\n=== KATEGORI KAMERA ===")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    pilih = input("Pilih kategori (nomor): ")

    if not pilih.isdigit() or int(pilih) < 1 or int(pilih) > len(categories):
        print("❌ Pilihan tidak valid!")
        return

    selected = categories[int(pilih) - 1]

    print(f"\n=== KAMERA KATEGORI {selected} ===")
    for cam in cameras:
        if cam["category"] == selected:
            print(f"- ID {cam['id']} | {cam['name']}")


def list_all_cameras():
    print("\n=== SEMUA KAMERA ===")
    for cam in cameras:
        print(f"- ID {cam['id']} | {cam['name']} ({cam['category']})")


# =========================
# ADMIN MENU
# =========================

def admin_menu():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Lihat Semua User & Vendor")
        print("2. Hapus Akun User/Vendor")
        print("3. Lihat Histori Penyewaan")
        print("4. Lihat Histori Transaksi")
        print("5. Logout")

        choice = input("Pilih menu: ")

        if choice == "1":
            list_all_users()
        elif choice == "2":
            delete_account()
        elif choice == "3":
            view_rental_history()
        elif choice == "4":
            view_transaction_history()
        elif choice == "5":
            print("👋 Keluar dari menu admin.\n")
            break
        else:
            print("❌ Pilihan tidak valid!\n")


def list_all_users():
    df = load_users()

    print("\n=== DAFTAR USER & VENDOR ===")

    if df.empty:
        print("📭 Belum ada user.")
        return

    for _, row in df.iterrows():
        print(f"- ID {row['id']} | {row['name']} ({row['role']})")



def delete_account():
    df = load_users()
    list_all_users()

    uid = input("Masukkan ID akun yang ingin dihapus: ")

    if not uid.isdigit():
        print("❌ ID tidak valid!")
        return

    uid = int(uid)

    user = df[df["id"] == uid]

    if user.empty:
        print("❌ ID tidak ditemukan!")
        return

    if user.iloc[0]["role"] == "admin":
        print("❌ Admin tidak boleh menghapus admin lainnya!")
        return

    df = df[df["id"] != uid]
    df.to_csv(FILE_PATH, index=False)

    print(f"🗑️ Akun '{user.iloc[0]['name']}' berhasil dihapus.")



def view_rental_history():
    print("\n=== HISTORI PENYEWAAN ===")
    if not rental_history:
        print("Belum ada histori penyewaan.")
        return

    for h in rental_history:
        print(f"- {h}")


def view_transaction_history():
    print("\n=== HISTORI TRANSAKSI ===")
    if not transaction_history:
        print("Belum ada transaksi.")
        return

    for t in transaction_history:
        print(f"- {t}")


# =========================
# VENDOR MENU
# =========================

def vendor_menu(user):
    while True:
        print("\n=== MENU VENDOR ===")
        print("1. Tambah Kamera")
        print("2. Hapus Kamera")
        print("3. Lihat Kamera Saya")
        print("4. Logout")

        choice = input("Pilih menu: ")

        if choice == "1":
            add_camera(user)
        elif choice == "2":
            delete_camera(user)
        elif choice == "3":
            list_my_cameras(user)
        elif choice == "4":
            print("👋 Keluar dari menu vendor.\n")
            break
        else:
            print("❌ Pilihan tidak valid!")


def add_camera(user):
    df = load_cameras()

    print("\n=== TAMBAH KAMERA ===")
    name = input("Nama kamera: ")
    category = input("Kategori kamera: ")

    new_id = df["id"].max() + 1 if not df.empty else 1

    new_camera = {
        "id": new_id,
        "name": name,
        "category": category,
        "vendor_id": user["id"]
    }

    df = pd.concat([df, pd.DataFrame([new_camera])], ignore_index=True)
    save_cameras(df)

    print(f"✨ Kamera '{name}' berhasil ditambahkan!")


def delete_camera():
    print("\n=== HAPUS KAMERA ===")
    list_all_cameras()

    cid = input("Masukkan ID kamera: ")

    if not cid.isdigit():
        print("❌ ID tidak valid!")
        return

    cid = int(cid)

    for cam in cameras:
        if cam["id"] == cid:
            cameras.remove(cam)
            print(f"🗑️ Kamera '{cam['name']}' berhasil dihapus!")
            return

    print("❌ Kamera tidak ditemukan!")

# =========================
# MAIN MENU
# =========================

def main_menu():
    while True:
        print("\n=== PHOVIAS CAMERA CARE ===")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            user = login_user()
            if user:
                if user["role"] == "user":
                    user_menu()
                elif user["role"] == "admin":
                    admin_menu()
                elif user["role"] == "vendor":
                    vendor_menu()
                else:
                    print(f"👉 Role '{user['role']}' belum punya menu.\n")

        elif choice == "2":
            register_user()

        elif choice == "3":
            print("Terima kasih telah menggunakan Phovias!")
            break

        else:
            print("❌ Pilihan tidak valid!\n")


# =========================
# RUN PROGRAM
# =========================
if __name__ == "__main__":
    main_menu()
