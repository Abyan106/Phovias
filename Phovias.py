# PHOVIAS
# Kelompok 3
# Atsilla Kaysa Asyraf
# Irenia Maisa Kamila
# Muhammad Abyan Daryansyah
# Najahah Patin
# Dzaky Hafidz Naufal

users = [
    {"id": 1, "name": "Admin", "role": "admin", "password": "admin123"},
    {"id": 2, "name": "Riko", "role": "vendor", "password": "vendor123"}
]

next_user_id = 3


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
                print(f"👉 Masuk ke menu {user['role']} (belum dibuat)\n")

        elif choice == "2":
            register_user()

        elif choice == "3":
            print("Terima kasih telah menggunakan Phovias!")
            break

        else:
            print("❌ Pilihan tidak valid!\n")


if __name__ == "__main__":
    main_menu()