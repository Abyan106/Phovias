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