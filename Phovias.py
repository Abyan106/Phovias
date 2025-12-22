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
VENDOR_FILE = "vendors.csv"
CAMERA_FILE = "cameras.csv"

def load_users():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["id", "name", "role", "password"])
        df.to_csv(FILE_PATH, index=False)
    return pd.read_csv(FILE_PATH)

def load_vendors():
    if not os.path.exists(VENDOR_FILE):
        df = pd.DataFrame(columns=["id", "user_id", "nama_toko", "deskripsi"])
        df.to_csv(VENDOR_FILE, index=False)
    return pd.read_csv(VENDOR_FILE)

def load_cameras():
    if not os.path.exists(CAMERA_FILE):
        df = pd.DataFrame(columns=["id", "name", "category", "vendor_id"])
        df.to_csv(CAMERA_FILE, index=False)
    return pd.read_csv(CAMERA_FILE)

def save_cameras(df):
    df.to_csv(CAMERA_FILE, index=False)

# Histori (didefinisikan agar tidak error saat diakses)
rental_history = []
transaction_history = []

# =========================
# USER AUTH FUNCTIONS
# =========================

def register_user():
    df = load_users()
    print ("=== Registrasi akun ===")

    name = input("Masukkan nama: ")
    password = input("Masukkan password: ")

    if name in df["name"].values:
        print("❌ Nama sudah terdaftar!\n")
        return

    new_id = df["id"].max() + 1 if not df.empty else 1

    new_user = {
        "id": new_id,
        "name": name,
        "role": "user",
        "password": password
    }

    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

    print(f"✅ Registrasi berhasil! Selamat datang, {name}.\n")


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

def register_vendor(user):
    df_users = load_users()
    df_vendors = load_vendors()

    if user ["role"] == "vendor" : 
        print("Kamu sudah menjadi vendor")
        return user
    
    print("=== Daftar menjadi vendor ===")
    store_name = input("nama toko: ")
    deskripsi = input ("deskrpisi toko: ")

    new_id = df_vendors["id"].max() + 1 if not df_vendors.empty else 1

    new_vendors = {
        "id": new_id,
        "user_id": user["id"],
        "nama_toko": store_name,
        "deskripsi": deskripsi
    }

    df_vendors = pd.concat([df_vendors, pd.DataFrame([new_vendors])], ignore_index=True)
    df_vendors.to_csv(VENDOR_FILE,index=False)

    df_users.loc [df_users["id"] == user["id"], "role"] = "vendor"
    df_users.to_csv(FILE_PATH,index=False)

    user["role"] = "vendor"
    print("Kamu berhasil berubah menjadi vendor")
    return user
    




def search_camera():
    df = load_cameras()
    key = input("Masukkan nama kamera: ").lower()

    print("\n=== HASIL PENCARIAN ===")

    result = df[df["name"].str.lower().str.contains(key, na=False)]

    if result.empty:
        print("❌ Kamera tidak ditemukan.")
        return

    for _, row in result.iterrows():
        print(f"- ID {row['id']} | {row['name']} ({row['category']})")



def list_categories():
    df = load_cameras()

    categories = sorted(df["category"].dropna().unique())

    print("\n=== KATEGORI KAMERA ===")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    pilih = input("Pilih kategori (nomor): ")

    if not pilih.isdigit() or not (1 <= int(pilih) <= len(categories)):
        print("❌ Pilihan tidak valid!")
        return

    selected = categories[int(pilih) - 1]

    print(f"\n=== KAMERA KATEGORI {selected} ===")
    result = df[df["category"] == selected]

    for _, row in result.iterrows():
        print(f"- ID {row['id']} | {row['name']}")


def list_all_cameras():
    df = load_cameras()

    print("\n=== SEMUA KAMERA ===")

    if df.empty:
        print("📭 Belum ada kamera.")
        return

    for _, row in df.iterrows():
        print(f"- ID {row['id']} | {row['name']} ({row['category']})")


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

    print(f"✨ Kamera '{name}' berhasil ditambahkan!")


def list_my_cameras(user):
    df = load_cameras()

    my_cameras = df[df["vendor_id"] == user["id"]]

    print("\n=== KAMERA SAYA ===")
    if my_cameras.empty:
        print("📭 Belum ada kamera.")
        return

    for _, cam in my_cameras.iterrows():
        print(f"- ID {cam['id']} | {cam['name']} ({cam['category']})")


def delete_camera(user):
    df = load_cameras()   # baca cameras.csv ke DataFrame

    print("\n=== HAPUS KAMERA ===")

    # buat nampilin kamera yang ada di vendor ini aja
    vendor_cameras = df[df["vendor_id"] == user["id"]]

    if vendor_cameras.empty:
        print("📭 Kamu belum punya kamera.")
        return

    for _, row in vendor_cameras.iterrows():
        print(f"- ID {row['id']} | {row['name']} ({row['category']})")

    cid = input("Masukkan ID kamera: ")

    if not cid.isdigit():
        print("❌ ID tidak valid!")
        return

    cid = int(cid)

    # cek apakah kamera kamera nya itu dari vendor ini bukan
    target = df[(df["id"] == cid) & (df["vendor_id"] == user["id"])]

    if target.empty:
        print("❌ Kamera tidak ditemukan atau bukan milikmu!")
        return

    # hapus kameranya
    df = df[df["id"] != cid]
    df.to_csv(CAMERA_FILE, index=False)

    print(f"🗑️ Kamera '{target.iloc[0]['name']}' berhasil dihapus!")


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
