# ==========================================
# PHOVIAS
# Kelompok 3
# Atsilla Kaysa Asyraf
# Irenia Maisa Kamila
# Muhammad Abyan Daryansyah
# Najahah Patin
# Dzaky Hafidz Naufal
# ==========================================

users = [
    {"id": 1, "name": "Admin", "role": "admin", "password": "admin123"},
    {"id": 2, "name": "Riko", "role": "vendor", "password": "vendor123"},
]

next_user_id = 3

cameras = [
    {"id": 1, "name": "Canon EOS R6", "category": "Mirrorless"},
    {"id": 2, "name": "Sony A6400", "category": "Mirrorless"},
    {"id": 3, "name": "Nikon D3500", "category": "DSLR"},
    {"id": 4, "name": "Fujifilm X100V", "category": "Compact"},
]


# =========================
# USER AUTH FUNCTIONS
# =========================

def register_user():
    global next_user_id
    print("\n=== REGISTRASI USER BARU ===")
    name = input("Masukkan nama: ")
    password = input("Masukkan password: ")

    users.append({
        "id": next_user_id,
        "name": name,
        "role": "user",
        "password": password
    })
    next_user_id += 1
    print(f"✅ Registrasi berhasil! Selamat datang, {name}.\n")


def login_user():
    print("\n=== LOGIN ===")
    name = input("Nama: ")
    password = input("Password: ")

    for u in users:
        if u["name"] == name and u["password"] == password:
            print(f"✅ Login berhasil! Halo, {u['name']} ({u['role']})\n")
            return u

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


def search_camera():
    key = input("Masukkan nama kamera: ").lower()
    print("\n=== HASIL PENCARIAN ===")
    found = False

    for cam in cameras:
        if key in cam["name"].lower():
            print(f"- {cam['name']} ({cam['category']})")
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
            print(f"- {cam['name']}")


def list_all_cameras():
    print("\n=== SEMUA KAMERA ===")
    for cam in cameras:
        print(f"- {cam['name']} ({cam['category']})")


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
                else:
                    print(f"👉 Menu {user['role']} belum dibuat.\n")

        elif choice == "2":
            register_user()

        elif choice == "3":
            print("Terima kasih telah menggunakan Phovias!")
            break

        else:
            print("❌ Pilihan tidak valid!\n")

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
    print("\n=== DAFTAR USER & VENDOR ===")
    for u in users:
        print(f"- ID {u['id']} | {u['name']} ({u['role']})")


def delete_account():
    list_all_users()
    uid = input("Masukkan ID akun yang ingin dihapus: ")

    if not uid.isdigit():
        print("❌ ID tidak valid!")
        return

    uid = int(uid)
    for u in users:
        if u["id"] == uid:
            if u["role"] == "admin":
                print("❌ Admin tidak boleh menghapus admin lainnya!")
                return
            users.remove(u)
            print(f"🗑️ Akun '{u['name']}' berhasil dihapus.")
            return

    print("❌ Akun tidak ditemukan!")


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
# RUN PROGRAM
# =========================
if __name__ == "__main__":
    main_menu()