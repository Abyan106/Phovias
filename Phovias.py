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

PRODUK_FILE = "produks.csv"

VENDOR_FILE = "vendors.csv"

def load_users():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["id", "email", "nama_depan","nama_belakang", "role", "password","ktp"])
        df.to_csv(FILE_PATH, index=False)
    return pd.read_csv(FILE_PATH)

def load_cameras():
    if not os.path.exists(PRODUK_FILE):
        df = pd.DataFrame(columns=["id", "vendor_id", "jenis_produk","kategori", "nama_produk", "deskripsi", "harga_sewa", "stok", "kondisi", "status"])
        df.to_csv(PRODUK_FILE, index=False)
    return pd.read_csv(PRODUK_FILE)

def load_vendors():
    if not os.path.exists(VENDOR_FILE):
        df = pd.DataFrame(columns=[
            "id", "user_id", "nama_toko", "deskripsi"
        ])
        df.to_csv(VENDOR_FILE, index=False)
    return pd.read_csv(VENDOR_FILE)


def save_cameras(df):
    df.to_csv(PRODUK_FILE, index=False)

def save_cameras(df):
    df.to_csv(PRODUK_FILE, index=False)

# Histori (didefinisikan agar tidak error saat diakses)
rental_history = []
transaction_history = []

# =========================
# USER AUTH FUNCTIONS
# =========================

def register_user():
    df = load_users()

    print("\n=== REGISTRASI AKUN ===")
    email = input("Masukkan email: ").strip().lower()
    nama_depan = input("Masukkan nama depan: ").strip()
    nama_belakang = input("Masukkan nama belakang: ").strip()
    ktp = input("Masukkan nomor KTP: ").strip()
    password = input("Masukkan password: ")

    # validasi sederhana
    if not nama_depan or not nama_belakang:
        print("❌ Nama depan dan belakang wajib diisi!\n")
        return

    if email in df["email"].values:
        print("❌ Email sudah terdaftar!\n")
        return

    new_id = df["id"].max() + 1 if not df.empty else 1

    new_user = {
        "id": new_id,
        "email" : email,
        "nama_depan": nama_depan,
        "nama_belakang": nama_belakang,
        "role": "user",
        "password": password,
        "ktp": ktp
    }

    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

    print(f"✅ Registrasi berhasil! Halo {nama_depan} {nama_belakang}, akun kamu siap dipakai.\n")


def login_user():
    df = load_users()

    print("\n=== LOGIN ===")
    email = input("Email: ").strip()

    user = df[df["email"] == email]

    if user.empty:
        print("❌ Email tidak terdaftar!\n")
        return None
    
    password = input("Password: ")

    if user.iloc[0]["password"] != password:
        print("❌ Password salah!\n")
        return None

    u = user.iloc[0]
    print(
        f"✅ Login berhasil! "
        f"Halo, {u['nama_depan']} {u['nama_belakang']} ({u['role']})\n"
    )

    return u.to_dict()


# =========================
# USER MENU (CAMERA)
# =========================

def user_menu(user):
    while True:
        print("\n=== MENU USER ===")
        print("1. Cari Kamera")
        print("2. Lihat Kategori Kamera")
        print("3. Lihat Semua Kamera")
        print("4. Daftar menjadi Vendor")
        print("5. Logout")

        choice = input("Pilih menu: ")

        if choice == "1":
            search_camera()
        elif choice == "2":
            list_categories()
        elif choice == "3":
            list_all_cameras()
        elif choice == "4":
            user = register_vendor(user)
            if user["role"] == "vendor":
                return
        elif choice == "5":
            print("👋 Keluar dari menu user.\n")
            break
        else:
            print("❌ Pilihan tidak valid!\n")

def register_vendor(user):
    df_users = load_users()
    df_vendors = load_vendors()

    if user["role"] == "vendor":
        print("❌ Kamu sudah menjadi vendor.\n")
        return user

    print("\n=== DAFTAR JADI VENDOR ===")
    store_name = input("Nama toko: ")
    description = input("Deskripsi toko: ")

    new_id = df_vendors["id"].max() + 1 if not df_vendors.empty else 1

    new_vendor = {
        "id": new_id,
        "user_id": user["id"],
        "nama_toko": store_name,
        "deskripsi": description
    }

    # simpan data toko ke csv
    df_vendors = pd.concat(
        [df_vendors, pd.DataFrame([new_vendor])],
        ignore_index=True
    )
    df_vendors.to_csv(VENDOR_FILE, index=False)

    # update role si user yang lagi login
    df_users.loc[df_users["id"] == user["id"], "role"] = "vendor"
    df_users.to_csv(FILE_PATH, index=False)

    user["role"] = "vendor"

    print("✅ Berhasil! Kamu sekarang VENDOR dan toko sudah dibuat.\n")
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
        print(f"- ID {row['id']} | {row['name']} ({row['kategori']})")



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
        print(f"- ID {row['id']} | {row['name']} ({row['kategori']})")


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

def vendor_entry_menu(user):
    while True:
        print("Pilih mode: ")
        print("1. Masuk sebagai Vendor")
        print("2. Masuk sebagai User")
        print("3. Kembali ke menu utama")

        choice = input("Pilih menu: ")
        if choice == "1":
            vendor_menu(user)
        elif choice == "2":
            user_menu(user)
        elif choice == "3":
            break
        else:
            print("❌ Pilihan tidak valid!\n")

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

    print("\n=== TAMBAH PRODUK ===")
    nama_produk = input("Nama produk: ")

    # PILIH JENIS PRODUK
    while True:
        print("\nJenis Produk:")
        print("1. Kamera")
        print("2. Lensa")
        pilih = input("Pilih (1/2): ")

        if pilih == "1":
            jenis_produk = "kamera"
            kategori_list = ["mirrorless", "dslr", "compact"]
            break
        elif pilih == "2":
            jenis_produk = "lensa"
            kategori_list = ["kit", "telephoto", "wide", "infrared"]
            break
        else:
            print("❌ Pilihan tidak valid! Masukkan 1 atau 2.")

    # PILIH KATEGORI (BERDASARKAN JENIS)
    while True:
        print("\nKategori:")
        for i, kat in enumerate(kategori_list, 1):
            print(f"{i}. {kat}")

        pilih_kat = input("Pilih kategori: ")

        if pilih_kat.isdigit() and 1 <= int(pilih_kat) <= len(kategori_list):
            kategori = kategori_list[int(pilih_kat) - 1]
            break
        else:
            print("❌ Kategori tidak valid!")

    deskripsi = input("Deskripsi: ")
    harga_sewa = input("Harga sewa: ")
    stok = input("Stok: ")
    kondisi = input("Kondisi: ")
    status = "tersedia"

    new_id = df["id"].max() + 1 if not df.empty else 1

    new_camera = {
        "id": new_id,
        "vendor_id": user["id"],
        "jenis_produk": jenis_produk,
        "kategori": kategori,
        "nama_produk": nama_produk,
        "deskripsi": deskripsi,
        "harga_sewa": harga_sewa,
        "stok": stok,
        "kondisi": kondisi,
        "status": status
    }

    df = pd.concat([df, pd.DataFrame([new_camera])], ignore_index=True)
    df.to_csv(PRODUK_FILE, index=False)

    ikon = "📷" if jenis_produk == "kamera" else "🔭"
    print(f"{ikon} {nama_produk} disimpan sebagai {jenis_produk.upper()} ({kategori})")


def list_my_cameras(user):
    df = load_cameras()

    my_products = df[df["vendor_id"] == user["id"]]

    print("\n=== PRODUK SAYA ===")

    if my_products.empty:
        print("📭 Belum ada produk.")
        return

    for _, p in my_products.iterrows():
        print(f"""
                ID            : {p['id']}
                Nama Produk   : {p['nama_produk']}
                Jenis Produk  : {p['jenis_produk']}
                Kategori      : {p['kategori']}
                Deskripsi     : {p['deskripsi']}
                Harga Sewa    : {p['harga_sewa']}
                Stok          : {p['stok']}
                Kondisi       : {p['kondisi']}
                Status        : {p['status']}
                ---------------------------------
                """)


def delete_camera(user):
    df = load_cameras()

    print("\n=== HAPUS PRODUK ===")

    vendor_products = df[df["vendor_id"] == user["id"]]

    if vendor_products.empty:
        print("📭 Kamu belum punya produk.")
        return

    for _, row in vendor_products.iterrows():
        print(f"- ID {row['id']} | {row['nama_produk']} ({row['jenis_produk']} - {row['kategori']})")

    cid = input("Masukkan ID produk: ")

    if not cid.isdigit():
        print("❌ ID tidak valid!")
        return

    cid = int(cid)

    target = df[(df["id"] == cid) & (df["vendor_id"] == user["id"])]

    if target.empty:
        print("❌ Produk tidak ditemukan atau bukan milikmu!")
        return

    nama_produk = target.iloc[0]["nama_produk"]

    df = df[df["id"] != cid]
    df.to_csv(PRODUK_FILE, index=False)

    print(f"🗑️ Produk '{nama_produk}' berhasil dihapus!")


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
                    user_menu(user)
                elif user["role"] == "vendor":
                    vendor_entry_menu(user)
                elif user["role"] == "admin":
                    admin_menu()

        elif choice == "2":
            register_user()

        elif choice == "3":
            print("Terima kasih telah menggunakan Phovias.")
            break
        else:
            print("❌ Pilihan tidak valid!")


# =========================
# RUN PROGRAM
# =========================
if __name__ == "__main__":
    main_menu()
    