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

RENTAL_FILE = "rentals.csv"

PEMBAYARAN_FILE = "pembayaran.csv"

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
            "id", "user_id", "nama_toko", "deskripsi", "alamat"
        ])
        df.to_csv(VENDOR_FILE, index=False)
    return pd.read_csv(VENDOR_FILE)

def load_rentals():
    if not os.path.exists(RENTAL_FILE):
        df = pd.DataFrame(columns=[
            "id", "user_id", "vendor_id", "produk_id", "tanggal_mulai", "tanggal_selesai", "alamat", "catatan", "total_harga", "status"
        ])
        df.to_csv(RENTAL_FILE, index=False)
    return pd.read_csv(RENTAL_FILE)

def load_pembayaran():
    if not os.path.exists(PEMBAYARAN_FILE):
        return pd.DataFrame(columns=[
            "id", "rental_id", "total_bayar",
            "metode", "status", "tanggal_bayar"
        ])
    return pd.read_csv(PEMBAYARAN_FILE)

def save_cameras(df):
    df.to_csv(PRODUK_FILE, index=False)

# =========================
# USER AUTH FUNCTIONS
# =========================

def register_user():
    df = load_users()

    print("\n=== REGISTRASI AKUN ===")
    email = input("Masukkan email: ").strip().lower()
    if email in df["email"].values:
        print("❌ Email sudah terdaftar!\n")
        return
    nama_depan = input("Masukkan nama depan: ").strip()
    nama_belakang = input("Masukkan nama belakang: ").strip()
    ktp = input("Masukkan nomor KTP: ").strip()
    password = input("Masukkan password: ")

    # validasi sederhana
    if not nama_depan or not nama_belakang:
        print("❌ Nama depan dan belakang wajib diisi!\n")
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
        print("2. Lihat Kategori barang")
        print("3. Lihat Semua barang")
        if user["role"] == "vendor":
            print("4. Kelola Toko Saya")
        else:
            print("4. Daftar jadi vendor")
        print("5. Bayar sewa")
        print("6. Konfirmasi terima barang")
        print("7. Kembalikan barang")
        print("8. Logout")

        choice = input("Pilih menu: ")

        if choice == "1":
            search_camera(user)
        elif choice == "2":
            list_categories(user)
        elif choice == "3":
            list_all_cameras(user)
        elif choice == "4":
            if user["role"] == "vendor":
                vendor_menu(user)
            else:
                user = register_vendor(user)
        elif choice == "5":
            bayar_sewa(user)
        elif choice == "6":
            konfirmasi_terima_barang(user)
        elif choice == "7":
            kembalikan_kamera(user)
        elif choice == "8":
            print("👋 Keluar dari menu user.\n")
            break
        else:
            print("❌ Pilihan tidak valid!\n")
    
def input_tanggal(label):
    print(f"\n{label} (ketik 'q' untuk batal)")

    # inputan buat tahun
    while True:
        tahun = input("Tahun (2026-2030): ").strip()
        if tahun.lower() == "q":
            return None
        if not tahun.isdigit():
            print("❌ Tahun harus angka.")
            continue

        tahun = int(tahun)
        if tahun < 2026 or tahun > 2030:
            print("❌ Tahun harus antara 2026 sampai 2030.")
            continue
        break

    # inputan buat bulan
    while True:
        bulan = input("Bulan (1-12): ").strip()
        if bulan.lower() == "q":
            return None
        if not bulan.isdigit():
            print("❌ Bulan harus angka.")
            continue

        bulan = int(bulan)
        if bulan < 1 or bulan > 12:
            print("❌ Bulan tidak valid.")
            continue
        break

    # inputan buat hari
    while True:
        hari = input("Hari: ").strip()
        if hari.lower() == "q":
            return None
        if not hari.isdigit():
            print("❌ Hari harus angka.")
            continue

        hari = int(hari)

        max_hari = 31
        if bulan in [4, 6, 9, 11]:
            max_hari = 30
        elif bulan == 2:
            max_hari = 29 
        if hari < 1:
            print("❌ Hari tidak valid. Tidak ada tanggal 0 atau negatif di kalender.")
            continue

        if hari > max_hari:
            print(
                f"❌ Bulan {bulan} hanya sampai tanggal {max_hari}. "
                "Tanggal yang kamu masukkan melebihi kalender."
            )
            continue
        break

    return f"{tahun:04d}-{bulan:02d}-{hari:02d}"
            
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
    users_df = load_users()

    if df.empty:
        print("Tidak ada produk.")
        return

    for kiri, row in df.iterrows():
        vendor = users_df[users_df["id"] == row["vendor_id"]]

        if not vendor.empty:
            nama_toko = vendor.iloc[0].get("nama_toko", "Vendor")
        else:
            nama_toko = "Vendor"

        print(
            f"- ID {row['id']} | "
            f"{row['nama_produk']} ({row['kategori']}) "
            f"-  {nama_toko}"
        )


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

def register_vendor(user):
    df_users = load_users()
    df_vendors = load_vendors()

    if user["role"] == "vendor":
        print("❌ Kamu sudah menjadi vendor.\n")
        return user

    print("\n=== DAFTAR JADI VENDOR ===")
    store_name = input("Nama toko: ")
    description = input("Deskripsi toko: ")
    alamat = input("Alamat toko: ")

    new_id = df_vendors["id"].max() + 1 if not df_vendors.empty else 1

    new_vendor = {
        "id": new_id,
        "user_id": user["id"],
        "nama_toko": store_name,
        "deskripsi": description,
        "alamat": alamat
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

def simpan_proposal_sewa(rental):
    df = load_rentals()
    new_id = df["id"].max() + 1 if not df.empty else 1

    rental["id"] = new_id
    rental["status"] = "menunggu_acc"

    df = pd.concat([df, pd.DataFrame([rental])], ignore_index=True)
    df.to_csv(RENTAL_FILE, index=False)


def ajukan_sewa(cam, user):
    print("\n=== AJUKAN SEWA ===")
    tgl_mulai = input_tanggal("Tanggal Mulai")
    if not tgl_mulai:
        print("❌ Pengajuan sewa dibatalkan.")
        return

    tgl_selesai = input_tanggal("Tanggal Selesai")
    if not tgl_selesai:
        print("❌ Pengajuan sewa dibatalkan.")
        return
    lama_sewa = input("Lama sewa (hari): ")

    if not lama_sewa.isdigit():
        print("❌ Lama sewa harus berupa angka.")
        return

    lama_sewa = int(lama_sewa)

    while True:
        print("\nAlasan Sewa:")
        print("1. Wedding")
        print("2. Belajar")
        print("3. Event")
        print("4. Konten / Sosial Media")
        print("5. Lainnya")
        print("q. Batal")

        pilih = input("Pilih alasan (1-5 / q): ").lower()

        if pilih == "q":
            print("❌ Pengajuan sewa dibatalkan.")
            return

        alasan_map = {
            "1": "wedding",
            "2": "belajar",
            "3": "event",
            "4": "konten",
            "5": "lainnya"
        }

        if pilih in alasan_map:
            alasan = alasan_map[pilih]
            break
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")


    alamat = input("Masukan alamat untuk pengiriman: ")
    catatan = ""
    while True:
        if alasan == "lainnya":
            catatan = input("Jelaskan alasan sewa (opsional / q untuk batal): ")
        else:
            catatan = input("Catatan tambahan (opsional / q untuk batal): ")

        if catatan.lower() == "q":
            print("❌ Pengajuan sewa dibatalkan.")
            return
        else:
            break

    harga_per_hari = int(cam["harga_sewa"])
    total_harga = harga_per_hari * lama_sewa

    rental = {
        "user_id": user["id"],
        "produk_id": cam["id"],
        "vendor_id": cam["vendor_id"],
        "tanggal_mulai": tgl_mulai,
        "tanggal_selesai": tgl_selesai,
        "alamat": alamat,
        "alasan": alasan,
        "catatan": catatan,
        "total_harga": total_harga
    }

    simpan_proposal_sewa(rental)

    print(f"💰 Total harga sewa: {total_harga}")
    print("📨 Proposal sewa dikirim ke vendor. Tunggu persetujuan.\n")
    
def search_camera(user):
    df = load_cameras()
    key = input("Masukkan nama kamera: ").lower()

    result = df[df["nama_produk"].str.lower().str.contains(key, na=False)]

    print("\n=== HASIL PENCARIAN ===")
    pilih_dan_baca_produk(result, user)

def list_categories(user):
    df = load_cameras()

    categories = sorted(df["kategori"].dropna().unique())

    print("\n=== KATEGORI PRODUK ===")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    pilih = input("Pilih kategori (nomor): ")

    if not pilih.isdigit() or not (1 <= int(pilih) <= len(categories)):
        print("❌ Pilihan tidak valid!")
        return

    selected = categories[int(pilih) - 1]
    result = df[df["kategori"] == selected]

    print(f"\n=== PRODUK KATEGORI {selected.upper()} ===")
    pilih_dan_baca_produk(result, user)

def list_all_cameras(user):
    df = load_cameras()

    print("\n=== SEMUA KAMERA ===")

    if df.empty:
        print("📭 Belum ada kamera.")
        return
    pilih_dan_baca_produk(df, user)

def bayar_sewa(user):
    df_rental = load_rentals()
    df_bayar = load_pembayaran()

    tagihan = df_rental[
        (df_rental["user_id"] == user["id"]) &
        (df_rental["status"] == "menunggu_pembayaran")
    ]

    if tagihan.empty:
        print("💤 Tidak ada sewa yang perlu dibayar.")
        return

    print("\n=== TAGIHAN SEWA ===")
    for kiri, row in tagihan.iterrows():
        print(f"""
ID Rental     : {row['id']}
Produk ID    : {row['produk_id']}
Tanggal      : {row['tanggal_mulai']} s/d {row['tanggal_selesai']}
Total Harga  : {row['total_harga']}
Status       : {row['status']}
-------------------------
""")

    #rid = rental id
    rid = input("Masukkan ID rental yang ingin dibayar (atau kosong): ")
    if not rid.isdigit():
        print("❌ Batal.")
        return

    rid = int(rid)
    rental = df_rental[df_rental["id"] == rid]

    if rental.empty:
        print("❌ Rental tidak ditemukan.")
        return

    print("\nMetode Pembayaran:")
    print("1. Transfer")
    print("2. E-Wallet")

    pilih = input("Pilih metode: ")

    metode_map = {
        "1": "transfer",
        "2": "e-wallet",
    }

    if pilih not in metode_map:
        print("❌ Metode tidak valid.")
        return

    metode = metode_map[pilih]

    tanggal_bayar = input("Tanggal bayar (YYYY-MM-DD): ").strip()

    new_id = df_bayar["id"].max() + 1 if not df_bayar.empty else 1

    pembayaran = {
        "id": new_id,
        "rental_id": rid,
        "total_bayar": rental.iloc[0]["total_harga"],
        "metode": metode,
        "status": "berhasil",
        "tanggal_bayar": tanggal_bayar
    }

    df_bayar = pd.concat(
        [df_bayar, pd.DataFrame([pembayaran])],
        ignore_index=True
    )
    df_bayar.to_csv(PEMBAYARAN_FILE, index=False)

    df_rental.loc[df_rental["id"] == rid, "status"] = "dibayar"
    df_rental.to_csv(RENTAL_FILE, index=False)

    print("💰 Pembayaran berhasil! Vendor akan segera mengirim barang.")

def konfirmasi_terima_barang(user):
    df = load_rentals()

    dikirim = df[
        (df["user_id"] == user["id"]) &
        (df["status"] == "dikirim")
    ]

    if dikirim.empty:
        print("📭 Tidak ada barang yang perlu dikonfirmasi.")
        return

    print("\n=== BARANG DALAM PENGIRIMAN ===")
    for kiri, row in dikirim.iterrows():
        print(f"""
ID Rental     : {row['id']}
Produk ID    : {row['produk_id']}
Vendor ID    : {row['vendor_id']}
Tanggal Sewa : {row['tanggal_mulai']} s/d {row['tanggal_selesai']}
Alamat       : {row['alamat']}
Status       : {row['status']}
-------------------------
""")
    
    #rid = rental id
    rid = input("Masukkan ID rental yang sudah diterima (atau kosong): ")
    if not rid.isdigit():
        print("❌ Batal.")
        return

    rid = int(rid)
    idx = df[df["id"] == rid].index

    if idx.empty:
        print("❌ Rental tidak ditemukan.")
        return
    
    if df.loc[idx[0], "user_id"] != user["id"]:
        print("❌ Ini bukan rental milikmu.")
        return

    if df.loc[idx[0], "status"] != "dikirim":
        print("❌ Status rental tidak valid untuk konfirmasi.")
        return

    yakin = input("Yakin barang sudah diterima? (y/n): ").lower()
    if yakin != "y":
        print("❌ Konfirmasi dibatalkan.")
        return

    df.loc[idx, "status"] = "diterima_user"
    df.to_csv(RENTAL_FILE, index=False)

    print("📦 Barang berhasil dikonfirmasi diterima. Sewa resmi dimulai.")

def kembalikan_kamera(user):
    df = load_rentals()

    aktif = df[
        (df["user_id"] == user["id"]) &
        (df["status"] == "diterima_user")
    ]

    if aktif.empty:
        print("📭 Tidak ada kamera yang sedang kamu sewa.")
        return

    print("\n=== SEWA AKTIF ===")
    for kiri, row in aktif.iterrows():
        print(f"""
ID Rental     : {row['id']}
Produk ID    : {row['produk_id']}
Vendor ID    : {row['vendor_id']}
Tanggal Sewa : {row['tanggal_mulai']} s/d {row['tanggal_selesai']}
Status       : {row['status']}
-------------------------
""")

    rid = input("Masukkan ID rental yang ingin dikembalikan (atau kosong): ")
    if not rid.isdigit():
        print("❌ Batal.")
        return

    rid = int(rid)
    idx = df[df["id"] == rid].index

    if idx.empty:
        print("❌ Rental tidak ditemukan.")
        return

    if df.loc[idx[0], "user_id"] != user["id"]:
        print("❌ Ini bukan rental milikmu.")
        return

    if df.loc[idx[0], "status"] != "diterima_user":
        print("❌ Rental ini belum bisa dikembalikan.")
        return

    yakin = input("Yakin ingin mengembalikan kamera? (y/n): ").lower()
    if yakin != "y":
        print("❌ Pengembalian dibatalkan.")
        return

    df.loc[idx, "status"] = "menunggu_konfirmasi"
    df.to_csv(RENTAL_FILE, index=False)

    print("🔁 Kamera berhasil dikembalikan. Menunggu konfirmasi vendor.")
    
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

    for kiri, row in df.iterrows():
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
    df = load_rentals()

    print("\n=== SEMUA RIWAYAT RENTAL ===")

    if df.empty:
        print("📭 Belum ada rental.")
        return

def view_transaction_history():
    df = load_pembayaran()

    print("\n=== SEMUA TRANSAKSI ===")

    if df.empty:
        print("📭 Belum ada transaksi.")
        return

# =========================
# VENDOR MENU
# =========================

def vendor_menu(user):
    while True:
        print("\n=== MENU VENDOR ===")
        print("1. Tambah Kamera")
        print("2. Hapus Kamera")
        print("3. Lihat Kamera Saya")
        print("4. Lihat proposal rental")
        print("5. Kirim barang (proposal disetujui)")
        print("6. Konfirmasi pengembalian barang")
        print("7. Logout")

        choice = input("Pilih menu: ")

        if choice == "1":
            add_camera(user)
        elif choice == "2":
            delete_camera(user)
        elif choice == "3":
            list_my_cameras(user)
        elif choice == "4":
            lihat_proposal_sewa(user)
        elif choice == "5":
            kirim_barang(user)
        elif choice == "6":
            konfirmasi_pengembalian(user)
        elif choice == "7":
            print("👋 Keluar dari menu vendor.\n")
            break
        else:
            print("❌ Pilihan tidak valid!")

def add_camera(user):
    df = load_cameras()

    print("\n=== TAMBAH PRODUK ===")
    nama_produk = input("Nama produk: ")

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
    while True:
        print("\nKondisi Produk:")
        print("1. Baru")
        print("2. Bekas")
        pilih_kondisi = input("Pilih (1/2): ")

        if pilih_kondisi == "1":
            kondisi = "baru"
            break
        elif pilih_kondisi == "2":
            kondisi = "bekas"
            break
        else:
            print("❌ Pilihan tidak valid! Masukkan 1 atau 2.")

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

    for kiri, p in my_products.iterrows():
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

    for kiri, row in vendor_products.iterrows():
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
    
def proses_proposal(pid):
    df = load_rentals()
    idx = df[df["id"] == pid].index

    if idx.empty:
        print("❌ Proposal tidak ditemukan.")
        return

    # VALIDASI STATUS
    if df.loc[idx[0], "status"] != "menunggu_acc":
        print("⚠️ Proposal ini sudah diproses sebelumnya.")
        return

    pilih = input("ACC proposal ini? (y/n): ").lower()

    if pilih == "y":
        df.loc[idx, "status"] = "menunggu_pembayaran"
        print("✅ Proposal disetujui. Menunggu pembayaran user.")
    elif pilih == "n":
        df.loc[idx, "status"] = "ditolak"
        print("❌ Proposal ditolak.")
    else:
        print("❌ Pilihan tidak valid.")
        return

    df.to_csv(RENTAL_FILE, index=False)

def lihat_proposal_sewa(user):
    df = load_rentals()
    proposals = df[df["vendor_id"] == user["id"]]

    if proposals.empty:
        print("📭 Tidak ada proposal.")
        return

    for kiri, row in proposals.iterrows():
        print(f"""
ID Proposal   : {row['id']}
Produk ID    : {row['produk_id']}
User ID      : {row['user_id']}
Tanggal      : {row['tanggal_mulai']} s/d {row['tanggal_selesai']}
Catatan      : {row['catatan']}
Status       : {row['status']}
-------------------------
""")

    pid = input("Masukkan ID proposal (atau kosong): ")
    if not pid.isdigit():
        return

    proses_proposal(int(pid))
    
def update_stok_kamera(produk_id, jumlah):
    df_cam = load_cameras()

    idx = df_cam[df_cam["id"] == produk_id].index
    if idx.empty:
        print("❌ Kamera tidak ditemukan.")
        return False

    stok_sekarang = int(df_cam.loc[idx[0], "stok"])
    stok_baru = stok_sekarang + jumlah

    if stok_baru < 0:
        print("❌ Stok kamera habis.")
        return False

    df_cam.loc[idx, "stok"] = stok_baru
    df_cam.to_csv(PRODUK_FILE, index=False)
    return True


def kirim_barang(user):
    df = load_rentals()

    siap_kirim = df[
        (df["vendor_id"] == user["id"]) &
        (df["status"].isin(["menunggu_pembayaran", "dibayar"]))
    ]

    if siap_kirim.empty:
        print("📭 Tidak ada proposal.")
        return

    print("\n=== PROPOSAL RENTAL ===")
    for kiri, row in siap_kirim.iterrows():
        catatan = ""
        if row["status"] != "dibayar":
            catatan = "❗ BELUM DIBAYAR"

        print(f"""
ID Proposal   : {row['id']}
Produk ID    : {row['produk_id']}
User ID      : {row['user_id']}
Tanggal      : {row['tanggal_mulai']} s/d {row['tanggal_selesai']}
Status       : {row['status']} {catatan}
-------------------------
""")
    #pid = proposal id
    pid = input("Masukkan ID proposal yang ingin dikirim (atau kosong): ")

    if not pid.isdigit():
        print("❌ Batal.")
        return

    pid = int(pid)
    idx = df[df["id"] == pid].index

    if idx.empty:
        print("❌ Proposal tidak ditemukan.")
        return

    # VALIDASI PEMBAYARAN
    if df.loc[idx[0], "status"] != "dibayar":
        print("💸 Barang belum dibayar. Tidak bisa dikirim.")
        return

    df.loc[idx, "status"] = "dikirim"
    df.to_csv(RENTAL_FILE, index=False)

    produk_id = df.loc[idx[0], "produk_id"]

    if not update_stok_kamera(produk_id, -1):
        print("❌ Gagal mengurangi stok kamera.")
        return

    print("🚚 Barang berhasil dikirim. Menunggu konfirmasi user apabila kamera telah sampai.")
    
def konfirmasi_pengembalian(user):
    df = load_rentals()

    menunggu_konfirmasi = df[
        (df["vendor_id"] == user["id"]) &
        (df["status"] == "dikembalikan")
    ]

    if menunggu_konfirmasi.empty:
        print("📭 Tidak ada pengembalian yang perlu dikonfirmasi.")
        return

    print("\n=== PENGEMBALIAN MENUNGGU KONFIRMASI ===")
    for kiri, row in menunggu_konfirmasi.iterrows():
        print(f"""
ID Rental     : {row['id']}
Produk ID    : {row['produk_id']}
User ID      : {row['user_id']}
Tanggal Sewa : {row['tanggal_mulai']} s/d {row['tanggal_selesai']}
Status       : {row['status']}
-------------------------
""")

    rid = input("Masukkan ID rental yang diterima kembali (atau kosong): ")
    if not rid.isdigit():
        print("❌ Batal.")
        return

    rid = int(rid)
    idx = df[df["id"] == rid].index

    if idx.empty:
        print("❌ Rental tidak ditemukan.")
        return

    if df.loc[idx[0], "vendor_id"] != user["id"]:
        print("❌ Ini bukan rental milikmu.")
        return

    if df.loc[idx[0], "status"] != "menunggu_konfirmasi":
        print("❌ Rental ini belum bisa dikonfirmasi.")
        return

    yakin = input("Konfirmasi kamera sudah diterima? (y/n): ").lower()
    if yakin != "y":
        print("❌ Konfirmasi dibatalkan.")
        return

    df.loc[idx, "status"] = "selesai"
    df.to_csv(RENTAL_FILE, index=False)

    produk_id = df.loc[idx[0], "produk_id"]

    if not update_stok_kamera(produk_id, 1):
        print("❌ Gagal menambah stok kamera.")
        return

    print("✅ Kamera diterima kembali. Rental dinyatakan SELESAI.")

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
                if user["role"] == "admin":
                    admin_menu()
                else:
                    user_menu(user)
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
    