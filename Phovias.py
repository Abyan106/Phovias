# ==========================================
# PHOVIAS
# Kelompok 3
# Atsilla Kaysa Asyraf
# Irenia Maisa Kamila
# Muhammad Abyan Daryansyah
# Najahah Patin
# Dzaky Hafidz Naufal
# ==========================================

# ==========================================
# IMPORTAN LIBRARY
# ==========================================
import pandas as pd
import numpy as np
import os

# ===========================================
# ASSET BUAT HEADER
# ===========================================
liner = "─" * 55
subliner = "-" * 55
miniliner = "─" * 30
indentasi = 55

# ===========================================
# LOAD DATA CSV
# ===========================================
FILE_PATH = "users.csv"

PRODUK_FILE = "produks.csv"

VENDOR_FILE = "vendors.csv"

RENTAL_FILE = "rentals.csv"

PEMBAYARAN_FILE = "pembayaran.csv"

RATING_FILE = "rating.csv"

def enterback():
    print("[Enter] back")
    
def enterback1():
    print("\n[Enter] back")
    
def opsi():
    print("\n[ID] detail")
    enterback()

def load_users():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["id", "email", "first_name","last_name", "role", "password","ktp"])
        df.to_csv(FILE_PATH, index=False)
    return pd.read_csv(FILE_PATH)

def load_cameras():
    if not os.path.exists(PRODUK_FILE):
        df = pd.DataFrame(columns=["id", "vendor_id", "product_types","category", "product_name", "description", "rental_fee", "stock", "condition", "status"])
        df.to_csv(PRODUK_FILE, index=False)
    return pd.read_csv(PRODUK_FILE)

def load_vendors():
    if not os.path.exists(VENDOR_FILE):
        df = pd.DataFrame(columns=[
            "id", "user_id", "shop_name", "description", "address"
        ])
        df.to_csv(VENDOR_FILE, index=False)
    return pd.read_csv(VENDOR_FILE)

def load_rentals():
    if not os.path.exists(RENTAL_FILE):
        df = pd.DataFrame(columns=[
            "id", "user_id", "vendor_id", "product_id", "start_date", "end_date", "address", "notes", "total_amount", "status","approval_date"
        ])
        df.to_csv(RENTAL_FILE, index=False)
    return pd.read_csv(RENTAL_FILE)

def load_pembayaran():
    if not os.path.exists(PEMBAYARAN_FILE):
        return pd.DataFrame(columns=[
            "id", "rental_id", "total_payment",
            "methods", "status", "payment_date"
        ])
    return pd.read_csv(PEMBAYARAN_FILE)

def load_ratings():
    if not os.path.exists(RATING_FILE):
        return pd.DataFrame(columns=[
            "id", "rental_id", "product_id",
            "vendor_id", "user_id", "rating","review"
        ])
    return pd.read_csv(RATING_FILE)

def save_users(df):
    df.to_csv(FILE_PATH, index=False)

def save_cameras(df):
    df.to_csv(PRODUK_FILE, index=False)
    
    
# =================================================
# PAGES SECTION
# =================================================
    
def paginate_select(df, render_func, per_page=5, title="DATA LIST", select_label="Select ID: "):
    """
    pagination buat selected
    """
    if df.empty:
        print("No data available.")
        enter_to_back()
        return None

    total_data = len(df)
    total_page = (total_data + per_page - 1) // per_page
    page = 0

    while True:
        start = page * per_page
        end = start + per_page
        page_data = df.iloc[start:end]

        print("\n" + liner)
        print(title.center(indentasi))
        print(f"Page {page + 1} of {total_page}".center(indentasi))
        print(liner)

        for kiri, row in page_data.iterrows():
            render_func(row)

        print("\n[n] Next     [p] Prev     [q] Quit")
        uid_input = input(select_label).strip().lower()

        if uid_input == "n":
            page = (page + 1) % total_page
        elif uid_input == "p":
            page = (page - 1) % total_page
        elif uid_input == "q":
            return None
        elif uid_input.isdigit():
            uid = int(uid_input)
            if uid in df["id"].values:
                return uid
            else:
                print("❌ Invalid User ID.")
        else:
            print("❌ Invalid input.")

def paginate(df, render_func, per_page=5, title="DATA LIST"):
    if df.empty:
        print("No data available.")
        enter_to_back()
        return

    total_data = len(df)
    total_page = (total_data + per_page - 1) // per_page
    page = 0

    while True:
        start = page * per_page
        end = start + per_page
        page_data = df.iloc[start:end]

        print("\n" + liner)
        print(title.center(indentasi))
        print(f"Page {page + 1} of {total_page}".center(indentasi))
        print(liner)

        for key, row in page_data.iterrows():
            render_func(row)

        print("\n[n] Next     [p] Prev     [q] Quit")
        cmd = input("> ").lower().strip()

        if cmd == "n":
            page = (page + 1) % total_page
        elif cmd == "p":
            page = (page - 1) % total_page
        elif cmd == "q":
            break
        else:
            print("Invalid input.")
    
# ==================================================
# BUTTON-BUTTON AN
# ==================================================
    
def enter_to_back(message=None):
    """
    * Return:
    * - None → user tekan Enter (back)
    """
    if message:
        print(message)

    print("\n[Enter] back")

    while True:
        pilihan = input("\n> ")
        if pilihan == "":
            return None
        else:
            print("Invalid choice")

def input_atau_back(df, message, id_label="ID"):
    """
    * NOTE BUAT ADMIN
    * Ini fungsi buat message kalo sebuah df (dataframe) kosong
    *z Pemakaian return:
    * - None = [Enter] back
    * - "retry" = kalo inputnya invalid
    * - int = kalo inputnya valid
    """
    if df.empty:
        print(message)
        enterback1()
        input("\n> ")
        return None
    
    pilihan = input("\n> ")
    
    if pilihan == "":
        return None
    
    if not pilihan.isdigit():
        print("Invalid.\n")
        return "retry"
    
    pilihan = int(pilihan)
    
    if pilihan not in df["id"].values:
        print(f"{id_label} not found.")
        return "retry"
    
    return pilihan

def confirm_action():
    """
    * Return:
    * - True  -> user pilih 'y'
    * - False -> user pilih 'n'
    """
    while True:
        choice = input("\n> ").lower().strip()

        if choice == "y":
            print("Confirmed.")
            return True
        elif choice == "n":
            print("Cancelled.")
            return False
        else:
            print("Invalid choice.")
            continue
        
# =========================
# USER AUTH FUNCTIONS
# =========================

def is_valid_username(username):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")

    for char in username:
        if char not in allowed_chars:
            return False
    return True

def is_valid_name(name):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")

    for char in name:
        if char not in allowed_chars:
            return False
    return True

# buah alamat
def is_valid_alamat(adress):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,-/ ")

    for char in adress:
        if char not in allowed_chars:
            return False
    return True

# nama toko
def is_valid_store_name(store_name):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ ")

    for char in store_name:
        if char not in allowed_chars:
            return False
    return True

def register_user():
    df = load_users()

    print(f"\n{liner}")
    print("MAKE YOUR ACCOUNT".center(indentasi))
    print("Input your information".center(indentasi))
    print(subliner)
    print("[q] to cancel registration at any time.")
    while True:
        email = input("\nEmail: ").strip().lower()

        if email.lower() == "q":
            print("Cancelled.\n")
            return
        
        # gak bisa kosong
        if not email:
            print("Email cannot be empty.\n")
            continue

        # biar gak bisa @gmail.com doang
        if email == "@gmail.com":
            print("Invalid email address. It must include a username.\n")
            continue

        # harus pake gmail.com
        if not email.endswith("@gmail.com"):
            print("Gmail address required. (@gmail.com)\n")
            continue

        # kalo udah terdaftar
        if email in df["email"].values:
            print("An account with this email already exists.\n")
            continue

        break
    
    while True:
        name = input("\nName: ").strip()

        if name.lower() == "q":
            print("Cancelled.\n")
            return
        
        if not name:
            print("Name cannot be empty.")
            continue

        if not is_valid_name(name):
            print(
                "Name can only contain letters and spaces"
            )
            continue
        break
    
    print("\nUsernames may contain letters, numbers, and underscores only")
    while True:
        username = input("Username: ").strip()

        if username.lower() == "q":
            print("Cancelled.\n")
            return
        
        if not username:
            print("Username cannot be empty.")
            continue

        if " " in username:
            print("Username cannot contain spaces.\n")
            continue
        
        if len(username) < 4:
            print("Username must be at least 4 characters long.\n")
            continue
        
        if len(username) > 20:
            print("Username cannot be longer than 20 characters.\n")
            continue

        if not is_valid_username(username):
            print("Username can only contain letters, numbers, and underscore.")
            continue
        
        if username in df["username"].values:
            print("Username already taken. Please choose another one.\n")
            continue

        break

    while True:
        id_card = input("\nID Card: ").strip()
        
        if id_card.lower() == "q":
            print("Cancelled.\n")
            return
        
        if not id_card:
            print("ID Card cannot be empty.\n")
            continue

        if not id_card.isdigit():
            print("ID Card must be a number\n.")
            continue

        if len(id_card) < 12 or len(id_card) > 18:
            print("ID Card must be between 12 and 18 digits.\n")
            continue
        
        ktp_sama = False

        for value in df["ktp"].values:
            if id_card == str(value):
                ktp_sama = True
                break

        if ktp_sama:
            print("An account with this ID Card already exists.\n")
            continue

        break


    while True:
        password = input("\nPassword: ")

        if password.lower() == "q":
                print("Cancelled.\n")
                return

        if not password:
            print("Password cannot be empty.")
            continue

        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            continue

        if len(password) > 32:
            print("Password cannot be longer than 32 characters.")
            continue
        break

    new_id = df["id"].max() + 1 if not df.empty else 91001

    new_user = {
        "id": new_id,
        "email": email,
        "name": name,
        "username": username,
        "role": "user",
        "password": password,
        "ktp": id_card
    }

    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

    print(f"\nRegistration successful.\nHello, {name}. Your account is ready to use.\n")


def login_user():
    df = load_users()

    print(f"\n{liner}")
    print("LOG IN".center(indentasi))
    print("Input your account".center(indentasi))
    print(subliner)
    email = input("Email: ").strip()

    if not email:
        print("Email cannot be empty.\n")
        return
    
    user = df[df["email"] == email]
    
    if user.empty:
        print("Account with this email does not exist.\n")
        return
    
    password = input("Password: ")

    if user.iloc[0]["password"] != password:
        print("Incorrect password.\n")
        return 

    u = user.iloc[0]
    print(f"\nLogin successful.\nHello there, {u['name']} ({u['role']}).\n")

    return u.to_dict()


# =========================
# USER MENU (CAMERA)
# =========================

def user_menu(user):
    while True:
        print(f"\n\n\n{liner}")
        print("USER MENU".center(indentasi))
        print(liner)
        print("1. Search product")
        print("2. Category product")
        print("3. All products")
        if user["role"] == "vendor":
            print("4. Lender menu")
        else:
            print("4. Register as Lender")
        print("5. Pay rental")
        print("6. Confirm receipt of goods")
        print("7. Return camera")
        print("8. Edit Profile")
        print("9. Log out")

        choice = input("\n> ")

        if choice == "1":
            hasil = search_camera(user)
            if hasil is None or hasil.empty:
                enter_to_back("📭 No products found.")
                continue
            pilih_dan_baca_produk(hasil, user)
            continue
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
            edit_profile_menu(user)
        elif choice == "9":
            print("Logged out.\n")
            break
        else:
            print("Your choice is invalid.\n")

 
def hari_dalam_bulan(bulan):
    if bulan == 2:
        return 28
    if bulan in [4]:
        return 30
    return 31

def tanggal_ke_hari(bulan, hari):
    total = 0

    for b in range(1, bulan):
        total += hari_dalam_bulan(b)

    total += hari
    return total

   
def input_tanggal(label):
    print(f"\n{label} (2026 only) [q] to cancel.\n")

    while True:
        bulan = input("Month (1-5): ").strip()
        if bulan.lower() == "q":
            return None, None
        if not bulan.isdigit():
            print("Month must be a number.")
            continue
        bulan = int(bulan)
        if not 1 <= bulan <= 5:
            print("Month must be 1-12.")
            continue
        break

    max_hari = hari_dalam_bulan(bulan)
    while True:
        hari = input(f"Day (1-{max_hari}): ").strip()
        if hari.lower() == "q":
            return None, None
        if not hari.isdigit():
            print("Day must be a number.")
            continue
        hari = int(hari)
        if not 1 <= hari <= max_hari:
            print(f"Invalid day. This month has {max_hari} days.")
            continue
        break

    tanggal_str = f"2026-{bulan:02d}-{hari:02d}"
    tanggal_int = tanggal_ke_hari(bulan, hari)
    return tanggal_str, tanggal_int

        
#! KELAR           
def view_camera_detail(cam, user):
    print("\n\n\nPRODUCT DETAILS")
    print(miniliner)
    print(f"""ID           : {cam['id']}
Name         : {cam['product_name']}
Types        : {cam['product_types']}
Category     : {cam['category']}
Description  : {cam['description']}
Rental Fee   : Rp{cam['rental_fee']}/day
Stock        : {cam['stock']}
Condition    : {cam['condition']}
Status       : {cam['status']}
""")

    if cam["status"] != "Available" or int(cam["stock"]) <= 0:
        print("Product is not available for rent.")
        return False

    print("Would you like to rent this product?")
    print("         [y] yes   [n] no")
    
    while True:
        pilih = input("\n> ").lower()

        if pilih == "y":
            success = ajukan_sewa(cam, user)
            return success
        elif pilih == "n":
            print("Cancelled.\n")    
            return True
        else:
            print("Invalid choice.")
            continue

#! KELAR
def pilih_dan_baca_produk(df, user):
    vendors_df = load_vendors()

    if df.empty:
        enter_to_back("📭 There are no products.")
        return

    def render_camera(row):
        vendor_id = int(row["vendor_id"])
        vendor = vendors_df[vendors_df["id"].apply(int) == vendor_id]

        if not vendor.empty:
            shop_name = vendor.iloc[0]["shop_name"]
        else:
            shop_name = "Vendor"

        print(f"- ID {row['id']} | {row['product_name']} ({row['category']}) - {shop_name}")

    while True:
        cam_id = paginate_select(
            df,
            render_func=render_camera,
            per_page=5,
            title="SEARCH RESULTS",
            select_label="Enter Product ID to view details or [q] to quit: "
        )

        if cam_id is None:
            return

        cam = df[df["id"] == cam_id]
        if not cam.empty:
            view_camera_detail(cam.iloc[0], user)
    
def ajukan_sewa(cam, user):
    print("\n\n\nRENTAL APPLICATION")
    print(miniliner)

    tgl_mulai_str, tgl_mulai_int = input_tanggal("Start Date")
    if tgl_mulai_str is None:
        print("Rental request cancelled.")
        return False

    tgl_selesai_str, tgl_selesai_int = input_tanggal("End Date")
    if tgl_selesai_str is None:
        print("Rental request cancelled.")
        return False

    if tgl_selesai_int <= tgl_mulai_int:
        print("End date must be after start date.")
        return False

    lama_sewa = tgl_selesai_int - tgl_mulai_int
    print(f"Rental duration: {lama_sewa} days")

    while True:
        print("\nReason for rental:")
        print("1. Wedding")
        print("2. Study")
        print("3. Event")
        print("4. Content / Social Media")
        print("5. Other")
        print("\n[q] Cancel.")
        pilih = input("\n> ").lower()

        if pilih == "q":
            print("Cancelled.")
            return False

        alasan_map = {
            "1": "wedding",
            "2": "study",
            "3": "event",
            "4": "content",
            "5": "other"
        }

        if pilih in alasan_map:
            alasan = alasan_map[pilih]
            break
        else:
            print("Invalid choice. Please select a valid reason.")


    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,-/ ")

    while True:
        address = input("Shipping address: ").strip()

        if address.lower() == "q":
            print("Rental request cancelled.\n")
            return

        if not address:
            print("Shipping address cannot be empty.\n")
            continue

        if len(address) < 10:
            print("Shipping address must be at least 10 characters long.\n")
            continue

        if not all(char in allowed_chars for char in address):
            print("Shipping address may contain letters, numbers, and spaces only.\n")
            continue

        break
    
    notes = ""
    while True:
        if alasan == "other":
            print("[q] Cancel.")
            notes = input("Describe your rental reason (optional): ")
        else:
            print("[q] Cancel.")
            notes = input("Additional notes (optional): ")

        if notes.lower() == "q":
            print("Cancelled.")
            return False
        else:
            break

    harga_per_hari = int(cam["rental_fee"])
    total_amount = harga_per_hari * lama_sewa

    rental = {
        "user_id": user["id"],
        "product_id": cam["id"],
        "vendor_id": cam["vendor_id"],
        "start_date": tgl_mulai_str,
        "end_date": tgl_selesai_str,
        "start_day_int": tgl_mulai_int,
        "end_day_int": tgl_selesai_int,
        "address": address,
        "alasan": alasan,
        "notes": notes,
        "total_amount": total_amount
    }

    simpan_proposal_sewa(rental)

    print(f"Total rental fee: {total_amount}")
    print("Your rental proposal has been sent to the lender. Waiting for approval.\n")
    return True

#! KELAR    
def search_camera(user):
    df = load_cameras()

    print("\nProduct name:")
    key = input("> ").lower()
    if key == "":
        print("Field must be input.")
        return

    results = []

    for index, row in df.iterrows():                    
        product_name = str(row["product_name"])
        if key in product_name.lower():
            results.append(row)

    if not results:
        print("Camera not found.")
        return

    return pd.DataFrame(results)


def register_vendor(user):
    df_users = load_users()
    df_vendors = load_vendors()

    if user["role"] == "vendor":
        print("You are already registered as a lender.\n")
        return user

    print("\n\n\nREGISTER AS LENDER")
    print(miniliner)
    print("[q] to cancel registration at any time.")

    # nama toko
    while True:
        store_name = input("\nStore name: ").strip()

        if store_name.lower() == "q":
            print("Registration cancelled.\n")
            return user
        
        if not is_valid_store_name(store_name):
            print("Store name may only contain letters, numbers, spaces, and underscore.")
            continue

        if not store_name:
            print("Store name cannot be empty.")
            continue

        if len(store_name) < 6:
            print("Store name must be at least 6 characters.")
            continue

        if len(store_name) > 20:
            print("Store name cannot exceed 20 characters.")
            continue
        break
    
    # deskripsi    
    description = input("\nStore description (optional): ").strip()
    if description.lower() == "q":
        print("Registration cancelled.\n")
        return user

    # alamat
    while True:
        address = input("\nVendor address: ").strip()

        if address.lower() == "q":
            print("Registration cancelled.\n")
            return user

        if not address:
            print("Address cannot be empty.")
            continue

        if len(address) < 10:
            print("Address must be at least 10 characters long.")
            continue

        if not is_valid_alamat(address):
            print(
                "Address may only contain letters, numbers, spaces, and characters (.,- /)."
            )
            continue
        break

    # bikin data vendor nya
    new_id = user["id"]  # <-- ganti ID vendor sama dengan ID user

    new_vendor = {
        "id": new_id,
        "user_id": user["id"],
        "shop_name": store_name,
        "description": description,
        "address": address
    }

    df_vendors = pd.concat(
        [df_vendors, pd.DataFrame([new_vendor])],
        ignore_index=True
    )
    df_vendors.to_csv(VENDOR_FILE, index=False)

    # UPDATE USER ROLE
    df_users.loc[df_users["id"] == user["id"], "role"] = "vendor"
    df_users.to_csv(FILE_PATH, index=False)

    user["role"] = "vendor"

    print("Registration successful. You are now a Lender.\n")
    return user

def simpan_proposal_sewa(rental):
    df = load_rentals()

    START_ID = 51001

    if df.empty:
        new_id = START_ID
    else:
        last_id = df["id"].max()
        new_id = last_id + 1 if last_id >= START_ID else START_ID

    rental["id"] = new_id
    rental["status"] = "Waiting for approval"

    df = pd.concat([df, pd.DataFrame([rental])], ignore_index=True)
    df.to_csv(RENTAL_FILE, index=False)


def list_categories(user):
    df = load_cameras()

    categories = sorted(df["category"].dropna().unique())

    print(f"\n\n\nPRODUCT CATEGORIES\n{miniliner}")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    print("\n[ID] to view products.")
    print("[Enter] back")
    pilih = input("\n> ")

    if pilih == "":
        return
    if not pilih.isdigit() or not (1 <= int(pilih) <= len(categories)):
        print("Your choice is invalid.")
        return

    selected = categories[int(pilih) - 1]
    result = df[df["category"] == selected]

    print(f"PRODUCT category {selected.upper()}")
    print(miniliner)
    pilih_dan_baca_produk(result, user)


def list_all_cameras(user):
    df = load_cameras()
    
    print("\nALL PRODUCTS")
    print(miniliner)

    if df.empty:
        print("📭 No products available.")
        return

    print("\nSORT BY:")
    print("1. Name (A-Z)")
    print("2. Rental Fee (Lowest)")
    print("3. Rental Fee (Highest)")
    print("4. Stock (Highest)")
    print("5. No Sorting")

    pilih = input("\n> ")

    if pilih == "1":
        df = df.sort_values(by="product_name")
    elif pilih == "2":
        df = df.sort_values(by="rental_fee")
    elif pilih == "3":
        df = df.sort_values(by="rental_fee", ascending=False)        
    elif pilih == "4":
        df = df.sort_values(by="stock", ascending=False)
    elif pilih == "5":
        pass                    
    else:
        print("Invalid choice.")
        return
    pilih_dan_baca_produk(df, user)

def input_payment_date_strict(start_day, approval_day):
    tahun, sm, sd = map(int, start_day.split("-"))
    tahun, am, ad = map(int, approval_day.split("-"))

    start_day_num = tanggal_ke_hari(sm, sd)
    approval_day_num = tanggal_ke_hari(am, ad)
    batas_pembayaran = start_day_num - 3

    while True:
        print("\nPAYMENT DATE INPUT")
        print("Rules:")
        print("- Payment must be AFTER approval")
        print("- Payment must be at least 3 days before rental start")
        print("[q] Cancel")

        bulan = input("Month (1-12): ").strip()
        if bulan.lower() == "q":
            return None
        if not bulan.isdigit():
            print("Month must be a number.")
            continue

        bulan = int(bulan)
        if bulan < 1 or bulan > 5:
            print("Month must be between 1 and 5.")
            continue

        if bulan < am:
            print("Payment month cannot be before approval month.")
            continue
        if bulan > sm:
            print("Payment month cannot be after rental start month.")
            continue

        hari = input("Day: ").strip()
        if hari.lower() == "q":
            return None
        if not hari.isdigit():
            print("Day must be a number.")
            continue

        hari = int(hari)
        if hari < 1 or hari > 31:
            print("Invalid day.")
            continue

        if bulan == am and hari < ad:
            print("Payment date cannot be before approval date.")
            continue

        if bulan == sm and hari > sd - 3:
            print("Payment must be at least 3 days before rental start.")
            continue

        payment_day = tanggal_ke_hari(bulan, hari)

        if payment_day == approval_day_num:
            return f"2026-{bulan:02d}-{hari:02d}"

        if payment_day < approval_day_num:
            print("Payment date cannot be before approval date.")
            continue

        if payment_day > batas_pembayaran:
            print("Payment must be at least 3 days before rental start.")
            continue

        return f"2026-{bulan:02d}-{hari:02d}"


def bayar_sewa(user):
    df_rental = load_rentals()
    df_bayar = load_pembayaran()

    tagihan = df_rental[
        (df_rental["user_id"] == user["id"]) &
        (df_rental["status"] == "Waiting for payment")
    ]

    if tagihan.empty:
        enter_to_back("📭 No rentals to be paid.")
        return

    print("\nRENTAL CHARGES")
    print(miniliner)
    for kiri, kanan in tagihan.iterrows():
        print(f"""Rental ID    : {kanan['id']}
Product ID   : {kanan['product_id']}
Date         : {kanan['start_date']} ─ {kanan['end_date']}
Total amount : {kanan['total_amount']}
Status       : {kanan['status']}
-------------------------
""")

    #rid = rental id
    print("\n[ID] to pay rental.\n[Enter] cancel.")
    rid = input("\n> ").strip()
    if not rid.isdigit():
        print("Cancelled.")
        return

    rid = int(rid)
    rental = df_rental[df_rental["id"] == rid]

    if rental.empty:
        print("Rental not found.")
        return

    print(f"\nPayment methods\n{miniliner}")
    print("1. Transfer")
    print("2. E-Wallet")

    pilih = input("\n> ")
    methods_map = {
        "1": "transfer",
        "2": "e-wallet",
    }

    if pilih not in methods_map:
        print("Invalid payment method.")
        return

    methods = methods_map[pilih]

    start_day = rental.iloc[0]["start_date"]
    approval_day = rental.iloc[0]["approval_date"]

    payment_date = input_payment_date_strict(start_day, approval_day)
    if not payment_date:
        return

    
    total_tagihan = rental.iloc[0]["total_amount"]

    while True:
        print(f"\nTotal bill : {total_tagihan}")
        print("Enter payment amount")
        print("[q] Cancel")

        bayar = input("> ").strip()

        if bayar.lower() == "q":
            print("Payment cancelled.")
            return

        if not bayar.isdigit():
            print("❌ Payment must be numeric.")
            continue

        bayar = int(bayar)

        if bayar != total_tagihan:
            print("❌ Amount does not match the bill.")
            continue
        break


    START_ID = 61001

    if df_bayar.empty:
        new_id = START_ID
    else:
        last_id = df_bayar["id"].max()
        new_id = last_id + 1 if last_id >= START_ID else START_ID

    pembayaran = {
        "id": new_id,
        "rental_id": rid,
        "total_payment": rental.iloc[0]["total_amount"],
        "methods": methods,
        "status": "success",
        "payment_date": payment_date
    }

    df_bayar = pd.concat(
        [df_bayar, pd.DataFrame([pembayaran])],
        ignore_index=True
    )
    df_bayar.to_csv(PEMBAYARAN_FILE, index=False)

    df_rental.loc[df_rental["id"] == rid, "status"] = "Paid"
    df_rental.to_csv(RENTAL_FILE, index=False)

    print("Lender will ship the item soon.")

def konfirmasi_terima_barang(user):
    df = load_rentals()

    sent = df[
        (df["user_id"] == user["id"]) &
        (df["status"] == "Sent")
    ]

    if sent.empty:
        enter_to_back("📭 No items to be confirmed.")
        return

    print(f"\n\n\nITEMS IN DELIVERY\n{miniliner}")
    for kiri, kanan in sent.iterrows():
        print(f"""Rental ID     : {kanan['id']}
Product ID    : {kanan['product_id']}
Lender ID     : {kanan['vendor_id']}
Rental date   : {kanan['start_date']} ─ {kanan['end_date']}
Address       : {kanan['address']}
Status        : {kanan['status']}
""")
    
    #rid = rental id
    print("[ID] to confirm receipt of goods.\n[Enter] cancel.")
    rid = input("\n> ")
    if not rid.isdigit():
        print("Cancelled.")
        return

    rid = int(rid)
    idx = df[df["id"] == rid].index

    if idx.empty:
        print("Rental not found.")
        return
    
    if df.loc[idx[0], "user_id"] != user["id"]:
        print("This rental does not belong to you.")
        return

    if df.loc[idx[0], "status"] != "Sent":
        print("Invalid rental status for confirmation.")
        return

    print("Are you sure you want to confirm receipt of the item?")
    print("              [y] yes       [n] no")
    yakin = input("\n> ").lower()
    if yakin == "y":
        df.loc[idx, "status"] = "Received by user"
        df.to_csv(RENTAL_FILE, index=False)
        print("Confirmed. Rental has officially started.")
        return
    
    if yakin == "n":
        print("Cancelled.")
        return
    
    if yakin != "y" and yakin != "n":
        print("Your choice is invalid.")
        return


    print("The item has been confirmed as received. The rental is now active.")

def rating_produk(user):
    print(f"LEAVE A RATING\n{miniliner}")
    while True:
        rating = input("Rating(1-5): ")
        if not rating.isdigit():
            print("Rating must be a number.")
            continue
        
        rating = int(rating)
        if rating < 1:
            print("Rating cannot be less than 1")
            continue
        
        if rating > 5:
            print("Rating cannot be more than 5")
            continue
        break
    
    
    print("[Enter] to leave a blank.")
    review = input("Review (optional): ")
    while True:
        print("Are you sure you want to submit this rating?")
        print("           [y] yes   [n] no")
        konfirmasi = input("\n>").lower().strip()
        if konfirmasi == "y":
            print("Rating sent")
            return{
                "rating": rating,
                "review": review,
            }
        elif konfirmasi == "n":
            print("Cancelled.")
            return None
        else:
            print("Your choice is invalid.")

def kembalikan_kamera(user):
    df = load_rentals()

    aktif = df[
        (df["user_id"] == user["id"]) &
        (df["status"] == "Received by user")
    ]

    if aktif.empty:
        enter_to_back("📭 You are not renting any products.")
        return

    print(f"\nACTIVE RENTALS\n{miniliner}")
    for kiri, kanan in aktif.iterrows():
        print(f"""
Rental ID     : {kanan['id']}
Product ID    : {kanan['product_id']}
Vendor ID     : {kanan['vendor_id']}
Rental date   : {kanan['start_date']} ─ {kanan['end_date']}
Status        : {kanan['status']}
-------------------------
""")

    print("\n[ID] to return rental.\n[Enter] cancel.")
    rid = input("\n> ")
    # if not rid.isdigit():
    #     print("Cancelled.")
    #     return
    if rid == "":
        print("Cancelled.")
        return
    else:
        if not rid.isdigit():
            print("Rental ID is not valid.")
            return

    rid = int(rid)
    idx = df[df["id"] == rid].index

    if idx.empty:
        print("Rental not found.")
        return
    if df.loc[idx[0], "user_id"] != user["id"]:
        print("This rental does not belong to you.")
        return
    if df.loc[idx[0], "status"] != "Received by user":
        print("This rental cannot be returned yet.")
        return

    while True:
        print("Are you sure you want to return the item?")
        print("         [y] yes       [n] no")
        yakin = input("\n> ").lower()

        if yakin == "y":
            break
        elif yakin == "n":
            print("Cancelled.")
            return
        else:
            print("Your choice is invalid.")

    df.loc[idx, "status"] = "Pending confirmation"
    df.to_csv(RENTAL_FILE, index=False)
    print("Thank you for returning the item. Kindly fill out the review below.\n")
    
    hasil_rating = rating_produk(user)
    
    if hasil_rating:
        rating_df = load_ratings()
        
        rating_baru = {
        "id": len(rating_df) + 1,
        "rental_id": rid,
        "product_id": df.loc[idx[0], "product_id"],
        "vendor_id": df.loc[idx[0], "vendor_id"],
        "user_id": user["id"],
        "rating": hasil_rating["rating"],
        "review": hasil_rating["review"],
        }
        
        rating_df = pd.concat([rating_df, pd.DataFrame([rating_baru])], ignore_index=True)
        rating_df.to_csv(RATING_FILE, index=False)

    # print("Item returned successfully. Waiting for vendor confirmation.")
    

def edit_profile_menu(user):
    while True:
        print("\nEDIT PROFILE")
        print(miniliner)
        print("1. Change username")
        print("2. Change password")
        print("3. Back")

        choice = input("\n> ").strip()

        if choice == "1":
            ubah_username(user)
        elif choice == "2":
            ubah_password(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
                
def ubah_username(user):
    df = load_users()

    print("\n[q] to cancel at anytime")
    while True:
        new_username = input("Enter new username: ").strip()

        if new_username.lower() == "q":
                print("Cancelled.\n")
                return
            
        if not new_username:
            print("Username cannot be empty.")
            continue

        if " " in new_username:
            print("Username cannot contain spaces.\n")
            continue
        
        if len(new_username) < 4:
            print("Username must be at least 4 characters long.\n")
            continue
        
        if len(new_username) > 20:
            print("Username cannot be longer than 20 characters.\n")
            continue

        if not is_valid_username(new_username):
            print("Username can only contain letters, numbers, and underscore.")
            continue
        
        if new_username in df["username"].values:
            print("Username already taken. Please choose another one.\n")
            continue

        if new_username in df["username"].values:
            print("Username is already taken.")
            return
        break
    
    df.loc[df["id"] == user["id"], "username"] = new_username
    save_users(df)

    user["username"] = new_username

    print("Username successfully updated.")
    print(f"New username: {new_username}")
        
def ubah_password(user):
    df = load_users()

    print("[q] to cancel at anytime.")
    old_password = input("Enter current password: ").strip()

    if old_password == "q":
        print("Cancelled.\n")
        return
    
    if old_password != user["password"]:
        print("Current password is incorrect.")
        return

    new_password = input("Enter new password: ").strip()

    if new_password == "q":
        print("Cancelled.\n")
        return
    
    if len(new_password) < 6:
        print("Password must be at least 6 characters long.")
        return

    df.loc[df["id"] == user["id"], "password"] = new_password
    save_users(df)

    user["password"] = new_password

    print("Password successfully updated.")

# =========================
# ADMIN MENU KELAAAAAAAAAAAARRRRRRRRRR
# =========================
 
#! KELAR    
def print_admin_menu():
    print(f"\n\n\n{liner}")
    print("ADMIN MENU".center(indentasi))
    print(liner)
    print("1. Show all users/vendors")
    print("2. Delete user/vendor account")
    print("3. Rental history")
    print("4. Transaction history")
    print("5. Log out")
    
def admin_menu():
    while True:
        print_admin_menu()
        
        while True:
            choice = input("\n> ")
            if choice in {"1", "2", "3", "4", "5"}:
                break
            else:
                print("Invalid choice")

        if choice == "1":
            list_all_users()
        elif choice == "2":
            delete_account()
        elif choice == "3":
            view_rental_history()
        elif choice == "4":
            view_transaction_history()
        elif choice == "5":
            print("Logged out.\n")
            return

#! KELAR

def render_user(row):
    print(f"- ID {row['id']} | {row['name']} ({row['role']})")

def list_all_users():
    df = load_users()
    paginate(
        df,
        render_func=render_user,
        per_page=5,
        title="USER & VENDOR LIST"
    )

#! KELAR
# DELETION PURPOSES
def show_users_simple():
    df = load_users()
    for key, value in df.iterrows():
        print(f"- ID {value['id']} | {value['name']} ({value['role']})")
        
def show_user_detail(uid):
    df = load_users()
    user = df[df["id"] == uid]
    
    if user.empty:
        enter_to_back("ID not found.")
        return False
    
    if user.iloc[0]["role"] == "admin":
        print("You don't have permission to delete admin accounts.")
        return False

    print(f"\n\n\nDETAIL ACCOUNT\n{miniliner}")
    print(f"""ID       : {user.iloc[0]['id']}
Name     : {user.iloc[0]['name']}
Username : {user.iloc[0]['username']}
Email    : {user.iloc[0]['email']}
Role     : {user.iloc[0]['role']}
ID Card  : {user.iloc[0]['ktp']}
""")
    return True

def render_user_for_delete(row):
    print(f"[{row['id']}] {row['name']} | {row['email']}")

def delete_account():
    df = load_users()

    if df.empty:
        print("📭 No users to delete.")
        enter_to_back()
        return

    while True:
        uid = paginate_select(
            df,
            render_user_for_delete,
            per_page=5,
            title="DELETE ACCOUNT",
            select_label="Enter User ID to delete or [q] to quit: "
        )

        if uid is None:
            return  # user quit

        if not show_user_detail(uid):
            continue

        print("Want to delete this account? [y/n]")
        if not confirm_action():
            continue

        df = df[df["id"] != uid]
        df.to_csv(FILE_PATH, index=False)

        print("Account deleted.")
        return



#! KELAR
# RENTAL PURPOSES
def show_rental_simple(rentals):
    df_users = load_users()
    df_vendors = load_vendors()
    df_products = load_cameras()

    for key, value in rentals.iterrows():
        user_row = df_users[df_users["id"] == value["user_id"]]
        username = user_row.iloc[0]["username"] if not user_row.empty else "Unknown user"

        vendor_row = df_vendors[df_vendors["user_id"] == value["vendor_id"]]
        vendor_name = vendor_row.iloc[0]["shop_name"] if not vendor_row.empty else "Unknown lender"

        product_row = df_products[df_products["id"] == value["product_id"]]
        product_name = product_row.iloc[0]["product_name"] if not product_row.empty else "Unknown product"

        print(f"- Rental ID {value['id']} | {product_name}, {vendor_name}, {username}, [{value['status']}]")

def show_rental_detail(rchoice):
    while True:
        df_rentals = load_rentals()
        df_users = load_users()
        df_vendors = load_vendors()
        df_products = load_cameras()

        rental = df_rentals[df_rentals["id"] == rchoice]
        
        if rental.empty:
            print("\nRental ID not found.")
            return
        
        r = rental.iloc[0]
        
        user_row = df_users[df_users["id"] == rental.iloc[0]["user_id"]]
        username = user_row.iloc[0]["username"] if not user_row.empty else "Unknown User"
        
        vendor_row = df_vendors[df_vendors["id"] == rental.iloc[0]["vendor_id"]]
        vendor_name = vendor_row.iloc[0]["shop_name"] if not vendor_row.empty else "Unknown Vendor"

        product_row = df_products[df_products["id"] == r["product_id"]]
        product_name = product_row.iloc[0]["product_name"] if not product_row.empty else "Unknown Product"
        
        print(f"\n\n\nRENTAL DETAILS\n{miniliner}")
        print(f"""Rental ID    : {r['id']}
Product      : {product_name} (ID {r['product_id']})
Vendor ID    : {vendor_name} (ID {r['vendor_id']})
User ID      : {username} (ID {r['user_id']})
Start Date   : {r['start_date']}
End Date     : {r['end_date']}
Reason       : {r['alasan']}
Notes        : {r['notes']}
Status       : {r['status']}
Address      : {r['address']}
Total Amount : Rp{r['total_amount']}
    """)
        
        enter_to_back()
        return

def view_rental_history():
    while True:
        df = load_rentals()

        #kalo kosong
        print(f"\n\n\nALL RENTALS HISTORY\n{liner}")
        if df.empty:
            enter_to_back("📭 No rentals yet.")
            return

        #kalo ada
        show_rental_simple(df)
        opsi()
        while True:
            hasil = input_atau_back(
                df, message=None, id_label="Rental ID"
            )
            if hasil is None:
                return
            if hasil == "retry":
                continue
            rchoice = hasil
            break
        
        show_rental_detail(rchoice)
        enter_to_back()

#! KELAR
# PAYMENT PURPOSES
def show_payment_simple(payments):
    for key, value in payments.iterrows():
        print(f"- Payment ID {value['id']} | RID {value['rental_id']}, {value['payment_date']} ({value['status']})")

def show_payment_detail(pchoice):
    while True:
        df_pay = load_pembayaran()
        df_rentals = load_rentals()
        df_products = load_cameras()
        df_vendors = load_vendors()
        df_users = load_users()
        
        pay = df_pay[df_pay["id"] == pchoice]
        if pay.empty:
            print("Payment ID not found.")
            return
        
        p = pay.iloc[0]
        
        rental = df_rentals[df_rentals["id"] == p["rental_id"]]
        if rental.empty:
            print("Associated rental not found.")
            return
        
        r = rental.iloc[0]
        
        user = df_users[df_users["id"] == r["user_id"]]
        username = user.iloc[0]["username"] if not user.empty else "Unknown User"

        vendor = df_vendors[df_vendors["id"] == r["vendor_id"]]
        vendor_name = vendor.iloc[0]["shop_name"] if not vendor.empty else "Unknown Vendor"
        
        product = df_products[df_products["id"] == r["product_id"]]
        product_name = product.iloc[0]["product_name"] if not product.empty else "Unknown Product"
        
        print(f"\n\n\nPAYMENT DETAILS\n{miniliner}")
        print(f"""Payment ID      : {p['id']}
Rental ID       : {p['rental_id']}
Product         : {product_name} (ID {r['product_id']})
Vendor          : {vendor_name} (ID {r['vendor_id']})
User            : {username} (ID {r['user_id']})
Total Payment   : Rp{p['total_payment']}
Payment Method  : {p['methods']}
Status          : {p['status']}
Payment Date    : {p['payment_date']}
    """)

        enter_to_back()
        return

def view_transaction_history():
    while True:
        df = load_pembayaran()

        print(f"\n\n\nALL TRANSACTION HISTORY\n{miniliner}")            
        if df.empty:
            enter_to_back("📭 No transaction yet.")
            return
        
        show_payment_simple(df)
        print("\n[PID] details")
        enterback()
        while True:
            hasil = input_atau_back(
                df, message=None, id_label="Payment ID"
            )
            if hasil is None:
                return
            if hasil == "retry":
                continue
            pchoice = hasil
            break
        
        show_payment_detail(pchoice)
        enter_to_back

# =========================
# VENDOR MENU
# =========================

def vendor_menu(user):
    while True:
        print(f"\n\n\n{liner}")
        print("LENDER MENU".center(indentasi))
        print(liner)
        print("1. Add product")
        print("2. Delete product")
        print("3. View my products")
        print("4. View rental proposals")
        print("5. Send product (proposal approved)")
        print("6. Confirm product return")
        print("7. View all product reviews")
        print("8. Edit product")
        print("9. Log out")

        choice = input("\n> ")

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
            lihat_review_vendor(user)
        elif choice == "8":
            edit_product(user)
        elif choice == "9":
            print("Exited vendor menu.\n")
            break
        else:
            print("Your choice is invalid.\n")

#! KELAR
def add_camera(user):
    df = load_cameras()

    print(f"\n\n\nADD NEW PRODUCT\n{miniliner}")
    print("[q] cancel at any time")
    
    product_name = input("\nProduct name: ")
    if product_name.lower() == "q":
        print("Cancelled.\n")
        return

    while True:
        product_name = input("Product name [q to cancel]: ").strip()

        if product_name.lower() == "q":
            print("Add product cancelled.")
            return

        if not product_name:
            print("Product name cannot be empty.")
            continue

        # cek redundansi (nama sama, vendor sama)
        duplikat = df[
            (df["vendor_id"] == user["id"]) &
            (df["product_name"].str.lower() == product_name.lower())
        ]

        if not duplikat.empty:
            print("❌ You already have a product with this name.")
            print("Please enter a different product name.")
            continue

        break

    # PRODUCT TYPES
    while True:
        print("\nProduct type:")
        print("1. Camera")
        print("2. Lens")
        pilih = input("\n> ")

        if pilih.lower() == "q":
            print("Cancelled.\n")
            return
        
        if pilih == "1":
            product_types = "Camera"
            category_list = ["Mirrorless", "DSLR", "Compact"]
            break
        elif pilih == "2":
            product_types = "Lens"
            category_list = ["Kit", "Telephoto", "Wide", "Infrared"]
            break
        else:
            print("Your choice is invalid.")

    # CATEGORY
    while True:
        print("\nCategory:")
        for i, kat in enumerate(category_list, 1):
            print(f"{i}. {kat}")

        pilih_kat = input("\n> ")

        if pilih_kat.lower() == "q":
            print("Cancelled.\n")
            return
        
        if pilih_kat.isdigit() and 1 <= int(pilih_kat) <= len(category_list):
            category = category_list[int(pilih_kat) - 1]
            break
        else:
            print("Category choice is invalid.")
            
    # SPECIFICATION
    print("\nSpecification: ")
    specc = input("> ")
    if specc.lower() == "q":
        print("Cancelled.\n")
        return
    
    # DESCRIPTION
    print("\nDescription: ")
    description = input("> ")
    if description.lower() == "q":
            print("Cancelled.\n")
            return
    
    # HARGA SEWA
    print("\nRental fee (per day): ")
    rental_fee = input("> ")
    if rental_fee.lower() == "q":
            print("Cancelled.\n")
            return
    
    # STOCK
    print("\nStock: ")
    stock = input("> ")
    if stock.lower() == "q":
            print("Cancelled.\n")
            return
    
    # CONDITION
    while True:
        print("\nProduct condition:")
        print("1. Excellent")
        print("2. Good")
        print("3. Fair")
        pilih_condition = input("\n> ")

        if pilih_condition.lower() == "q":
            print("Cancelled.\n")
            return
        if pilih_condition == "1":
            condition = "Excellent"
            break
        elif pilih_condition == "2":
            condition = "Good"
            break
        elif pilih_condition == "3":
            condition = "Fair"
            break
        else:
            print("Invalid choice.")

    if int(stock) > 0:
        status = "Available"
    else:
        status = "Unavailable"


    START_ID = 71001

    if df.empty:
        new_id = START_ID
    else:
        last_id = df["id"].max()
        new_id = last_id + 1 if last_id >= START_ID else START_ID

    new_camera = {
        "id": new_id,
        "vendor_id": user["id"],
        "product_types": product_types,
        "category": category,
        "product_name": product_name,
        "specification": specc,
        "description": description,
        "rental_fee": rental_fee,
        "stock": stock,
        "condition": condition,
        "status": status
    }

    df = pd.concat([df, pd.DataFrame([new_camera])], ignore_index=True)
    df.to_csv(PRODUK_FILE, index=False)

    ikon = "📷" if product_types == "Camera" else "🔭"
    print(f"{ikon} {product_name} has been added as {product_types.lower()} ({category})")

def list_my_cameras(user):
    df = load_cameras()

    my_products = df[df["vendor_id"] == user["id"]]

    print(f"\n\n\nPRODUCTS DETAILS\n{miniliner}")

    if my_products.empty:
        print("📭 No products available.")
        return

    for key, value in my_products.iterrows():
        print(f"""ID            : {value['id']}
Name          : {value['product_name']}
Type          : {value['product_types']}
Category      : {value['category']}
Specification : {value['specification']}
Description   : {value['description']}
Rental Fee    : {value['rental_fee']}
Stock         : {value['stock']}
Condition     : {value['condition']}
Status        : {value['status']}
                """)

def delete_camera(user):
    df = load_cameras()

    print(f"\n\n\nDELETE PRODUCT\n{miniliner}")

    vendor_products = df[df["vendor_id"] == user["id"]]

    if vendor_products.empty:
        print("📭 No products available.")
        enter_to_back()
        return

    for kiri, value in vendor_products.iterrows():
        print(f"- ID {value['id']} | {value['product_name']} ({value['product_types']} - {value['category']})")

    while True:
        opsi()
        cid = input("\n> ").strip()

        if cid == "":
            return
        if not cid.isdigit():
            print("Invalid ID.")
            continue

        cid = int(cid)

        target = df[(df["id"] == cid) & (df["vendor_id"] == user["id"])]
        if target.empty:
            print("Product not found or not owned by you.")
            continue

        print("Are you sure you want to delete this product? [y/n]")
        if not confirm_action():
            return

        product_name = target.iloc[0]["product_name"]
        df = df[df["id"] != cid]
        df.to_csv(PRODUK_FILE, index=False)

        print(f"{product_name} has been removed.")
        break
    
def proses_proposal(pid):
    df = load_rentals()
    idx = df[df["id"] == pid].index

    if idx.empty:
        enter_to_back("📭 Proposal not found.")
        return

    if df.loc[idx[0], "status"] != "Waiting for approval":
        print("This proposal has been handled before.")
        return

    # print("\nApprove this rental proposal?")
    # print("     [y] yes   [n] no   [q] cancel")

    while True:
        choice = input("\n> ").lower().strip()

        if choice == "q":
            print("Cancelled.")
            return

        if choice == "y":
            print("\nApproval date (system input)")

            bulan = int(input("Month (1-12): "))
            if bulan == "q":
                print("Cancelled.\n")
                return
            
            hari = int(input("Day   : "))

            approval_date_str = f"2026-{bulan:02d}-{hari:02d}"

            df.loc[idx, "status"] = "Waiting for payment"
            df.loc[idx, "approval_date"] = approval_date_str

            print("Approved. Waiting for user payment.")
            break

        if choice == "n":
            df.loc[idx, "status"] = "Rejected"
            break

        print("Invalid choice.")

    df.to_csv(RENTAL_FILE, index=False)

def lihat_proposal_sewa_simpel(proposals):
    print("\nPROPOSAL LIST")
    print(liner)

    for key, value in proposals.iterrows():
        print(f"- Proposal ID {value['id']} | Product ID {value['product_id']} ({value['status']})"
        )

def lihat_proposal_detail(pid):
    df = load_rentals()
    proposal = df[df["id"] == pid]
    

    if proposal.empty:
        enter_to_back("Proposal not found.")
        return False

    p = proposal.iloc[0]

    print(f"\n\n\nPROPOSAL DETAIL\n{miniliner}")
    print(f"""Proposal ID : {p['id']}
Product ID  : {p['product_id']}
User ID     : {p['user_id']}
Date        : {p['start_date']} ─ {p['end_date']}
Notes       : {p['notes']}
Status      : {p['status']}
""")
    
    return True


def lihat_proposal_sewa(user):
    df = load_rentals()

    proposals = df[
        (df["vendor_id"] == user["id"]) &
        (df["status"] == "Waiting for approval")
    ]

    if proposals.empty:
        enter_to_back("📭 No proposals.")
        return

    while True:
        lihat_proposal_sewa_simpel(proposals)
        opsi()

        hasil = input_atau_back(
            proposals, message=None, id_label="Proposal ID"
        )

        if hasil is None:
            return

        if hasil == "retry":
            continue

        pid = hasil

        if not lihat_proposal_detail(pid):
            continue

        print("\nProcess this proposal?")
        print("    [y] yes   [n] no")

        proses_proposal(pid)
        return
    
def update_stock_kamera(product_id, jumlah):
    df_cam = load_cameras()

    idx = df_cam[df_cam["id"] == product_id].index
    if idx.empty:
        print("Product not found.")
        return False

    stock_sekarang = int(df_cam.loc[idx[0], "stock"])
    stock_baru = stock_sekarang + jumlah

    if stock_baru < 0:
        print("Insufficient stock.")
        return False

    df_cam.loc[idx, "stock"] = stock_baru
    df_cam.to_csv(PRODUK_FILE, index=False)
    return True


def kirim_barang(user):
    df = load_rentals()

    siap_kirim = df[
        (df["vendor_id"] == user["id"]) &
        (df["status"].isin(["Waiting for payment", "Paid"]))
    ]

    if siap_kirim.empty:
        print("📭 No proposal.")
        enter_to_back()
        return

    print(f"\n\n\nRENTAL PROPOSAL\n{miniliner}")
    for kiri, value in siap_kirim.iterrows():
        print(f"""Proposal ID  : {value['id']}
Product ID   : {value['product_id']}
User ID      : {value['user_id']}
Date         : {value['start_date']} ─ {value['end_date']}
Status       : {value['status']}
-------------------------
""")

    while True:
        opsi()
        pid = input("\n> ").strip()

        if pid == "":
            return

        if not pid.isdigit():
            print("Invalid proposal ID.")
            continue

        pid = int(pid)
        idx = df[df["id"] == pid].index

        if idx.empty:
            print("Proposal not found.")
            continue

        if df.loc[idx[0], "status"] != "Paid":
            print("The product has not been paid for yet. Cannot be sent.")
            return

        df.loc[idx, "status"] = "Sent"
        df.to_csv(RENTAL_FILE, index=False)

        update_stock_kamera(df.loc[idx[0], "product_id"], -1)
        print("🚚 Product sent.")
        break
    
def konfirmasi_pengembalian(user):
    df = load_rentals()

    pending = df[
        (df["vendor_id"] == user["id"]) &
        (df["status"] == "Pending confirmation")
    ]

    if pending.empty:
        enter_to_back("📭 No pending return confirmations")
        return

    print(f"\n\n\nRETURN CONFIRMATION QUEUE\n{miniliner}")
    for kiri, value in pending.iterrows():
        print(f"""Rental ID    : {value['id']}
Product ID   : {value['product_id']}
User ID      : {value['user_id']}
Rental date  : {value['start_date']} ─ {value['end_date']}
Status       : {value['status']}
""")

    while True:
        opsi()
        rid = input("\n> ").strip()

        if rid == "":
            return

        if not rid.isdigit():
            print("Invalid Rental ID.")
            continue

        rid = int(rid)
        idx = df[df["id"] == rid].index

        if idx.empty:
            print("Rental not found.")
            continue

        print("Confirm product has been returned? [y/n]")
        if not confirm_action():
            return

        df.loc[idx, "status"] = "Completed"
        df.to_csv(RENTAL_FILE, index=False)

        update_stock_kamera(df.loc[idx[0], "product_id"], 1)
        print("Product returned. Rental completed.")
        break

def lihat_review_vendor(user):
    df_rating = load_ratings()
    camera_df = load_cameras()
    user_df = load_users()

    review_vendor = df_rating[df_rating["vendor_id"] == user["id"]]

    print(f"\n\n⭐ REVIEW & RATING SUMMARY\n{miniliner}")

    if review_vendor.empty:
        print("📭 No reviews available.")
        return
    
    # dropna()=  ngebuang data kosong
    ratings = np.array(review_vendor["rating"].dropna(), dtype=int)

    print(f"""
Total reviews : {ratings.size}
Average rating: {np.mean(ratings):.2f}
Highest rating: {np.max(ratings)}
Lowest rating : {np.min(ratings)}
""")

    print(f"\n\nPRODUCT REVIEWS\n{miniliner}")

    for _, row in review_vendor.iterrows():

        cam = camera_df[camera_df["id"] == row["product_id"]]
        product_name = (
            cam.iloc[0]["product_name"]
            if not cam.empty and "product_name" in cam.columns
            else "Product"
        )

        reviewer = user_df[user_df["id"] == row["user_id"]]
        name_user = reviewer.iloc[0]["name"] if not reviewer.empty else "User"

        print(f"""Produk   : {product_name}
From     : {name_user}
Rating   : {row['rating']}
Review   : {row['review'] if row['review'] else '-'}
""")
    enter_to_back()
        
def edit_product(user):
    df = load_cameras()
    
    my_products = df[df["vendor_id"] == user["id"]]

    if my_products.empty:
        print("No products to edit.")
        enterback1()
        input()
        return

    print("\nEDIT PRODUCT")
    print(miniliner)
    for kiri, produk in my_products.iterrows():
        print(f"- ID {produk['id']} | {produk['product_name']}")

    print()
    opsi()
    pid = input("> ").strip()

    if pid == "":
        return

    if not pid.isdigit():
        print("Invalid ID.")
        enterback1()
        input()
        return

    pid = int(pid)
    idx_list = df[(df["id"] == pid) & (df["vendor_id"] == user["id"])].index
    if idx_list.empty:
        print("Product not found or not owned by you.")
        enterback1()
        input()
        return

    idx = idx_list[0]


    # ===== EDIT MODE =====
    while True:
        print("""
EDIT MENU
1. Product name
2. Description
3. Specification
4. Rental fee
5. Stock
6. Status (Available / Unavailable)
7. Condition
[q] Finish editing
""")

        choice = input("> ").strip().lower()
        print("\n[q] to cancel at anytime.")

        if choice == "1":
            while True:
                vendor_id = user["id"]
                print("\nNew product name: ")
                nama_produk_baru = input("> ")
                
                if nama_produk_baru == "q":
                    print("Cancelled.")
                    break
                
                if nama_produk_baru == "":
                    print("Product name cannot be empty.\n")
                    continue
                
                is_duplicate = df[
                (df["vendor_id"] == vendor_id) &
                (df["product_name"].str.lower() == nama_produk_baru.lower()) &
                (df.index != idx)
        ]

                if not is_duplicate.empty:
                    print("Product name already exist in your store.")
                    continue

                df.loc[idx, "product_name"] = nama_produk_baru
                print("Product name updated.")
                break
            
        elif choice == "2":
            while True:
                desc = input("New description (min 20 chars): ").strip()

                if desc.lower() == "q":
                    print("Cancelled.")
                    break

                if desc == "":
                    print("Description cannot be empty.")
                    continue

                if len(desc) < 20:
                    print("Description must be at least 20 characters.")
                    continue

                df.loc[idx, "description"] = desc
                print("Description updated.")
                break

        elif choice == "3":
            while True:
                spec = input("New specification (min 20 chars): ").strip()

                if spec.lower() == "q":
                    print("Cancelled.")
                    break

                if spec == "":
                    print("Specification cannot be empty.")
                    continue

                if len(spec) < 20:
                    print("Specification must be at least 20 characters.")
                    continue

                df.loc[idx, "specification"] = spec
                print("Specification updated.")
                break

        elif choice == "4":
            fee = input("New rental fee: ").strip()
            if fee == "q":
                print("Cancelled.")
                return
            if not fee.isdigit():
                print("Rental fee must be a number.")
                continue
            df.loc[idx, "rental_fee"] = int(fee)

        elif choice == "5":
            stock = input("New stock: ").strip()
            if stock == "q":
                print("Cancelled.")
                return
            if not stock.isdigit():
                print("Stock must be a number.")
                continue

            stock = int(stock)
            df.loc[idx, "stock"] = stock
            df.loc[idx, "status"] = "Available" if stock > 0 else "Unavailable"

        elif choice == "6":
            print("\nStatus:\n1. Available\n2. Unavailable")
                
            while True:
                status = input("> ").strip().lower()
                if status == "q":
                    print("Cancelled.")
                    break
                if status == "1":
                    df.loc[idx, "status"] = "Available"
                    break
                if status == "2":
                    df.loc[idx, "status"] = "Unavailable"
                    break
                if status == "":
                    print("Cannot be empty.")
                    continue
            
                print("Invalid choice.")
                    
        
        elif choice == "7":
            print("1. Excellent\n2. Good\n3. Fair")
            condition = input("> ").strip()
            mapping = {"1": "Excellent", "2": "Good", "3": "Fair"}
            if condition not in mapping:
                print("Invalid choice.")
                continue
            df.loc[idx, "condition"] = mapping[condition]

        elif choice == "q":
            df.to_csv(PRODUK_FILE, index=False)
            print("All changes saved.")
            break

        else:
            print("Invalid option.")
            continue

        # simpan SETIAP edit
        df.to_csv(PRODUK_FILE, index=False)
        print("Product updated successfully.")


# =========================
# MAIN MENU
# =========================

def main_menu():
    while True:
        print(f"\n\n\n{liner}")
        print("PHOVIAS CAMERA CARE".center(indentasi))
        print(liner)
        print("1. Log in")
        print("2. Register")
        print("3. Exit")

        choice = input("\n> ")

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
            print("See you!")
            break
        else:
            print("Your choice is invalid.\n")

# =========================
# RUN PROGRAM
# =========================
if __name__ == "__main__":
    main_menu()
    