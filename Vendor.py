# =========================
# VENDOR MENU
# =========================

def vendor_menu():
    while True:
        print("\n=== MENU VENDOR ===")
        print("1. Tambah Kamera")
        print("2. Hapus Kamera")
        print("3. Lihat Semua Kamera")
        print("4. Logout")

        choice = input("Pilih menu: ")

        if choice == "1":
            add_camera()
        elif choice == "2":
            delete_camera()
        elif choice == "3":
            list_all_cameras()
        elif choice == "4":
            print("👋 Keluar dari menu vendor.\n")
            break
        else:
            print("❌ Pilihan tidak valid!\n")