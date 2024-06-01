import csv
import pwinput
from prettytable import PrettyTable
import sys
import datetime

daftar_barang=[]
akun_admin=[]
akun_pelanggan=[]
keranjang=[]

def is_working_hours():
    now = datetime.datetime.now()
    start_time = datetime.datetime(now.year, now.month, now.day, 8, 0)  # 08:00 AM
    end_time = datetime.datetime(now.year, now.month, now.day, 16, 0)   # 04:00 PM
    return start_time <= now <= end_time

def simpan_daftar_barang():
    with open("databarang.csv", "w", newline="") as new_file:
        fieldNames = ["nama", "harga", "jenis", "stock"]
        csv_writer = csv.DictWriter(
            new_file, delimiter=",", fieldnames=fieldNames)
        csv_writer.writeheader()
        for i in daftar_barang:
            csv_writer.writerow(i)

def simpan_daftar_pelanggan():
    with open("datapelanggan.csv", "w", newline="") as new_file:
        fieldNames = ["nama", "sandi" ,"saldo", "e-money", "pin", "umur", "gender"]
        csv_writer = csv.DictWriter(
            new_file, delimiter=",", fieldnames=fieldNames)
        csv_writer.writeheader()
        for i in akun_pelanggan:
            csv_writer.writerow(i)

def ambil_data_barang_csv():
    with open('databarang.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        daftar_barang.clear()
        for row in reader:
            daftar_barang.append(dict(row))

def ambil_data_pelanggan_csv():
    with open('datapelanggan.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        akun_pelanggan.clear()
        for row in reader:
            akun_pelanggan.append(dict(row))

def ambil_data_admin_csv():
    with open('dataadmin.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        akun_admin.clear()
        for row in reader:
            akun_admin.append(dict(row))

def tampil_data_barang():
    table = PrettyTable()
    table.title = "Daftar Barang"
    table.field_names = ["Nomor","Nama barang", "Harga","Stock","Jenis"]
    for i in range(len(daftar_barang)):
        table.add_row([i+1,daftar_barang[i]["nama"], "Rp"+ str(daftar_barang[i]["harga"]),daftar_barang[i]["stock"],daftar_barang[i]["jenis"]])
    print(table)

def tambah_data_barang():
    while True:
        tampil_data_barang()
        try:
            baru = {}
            nama = str(input("masukkan nama : "))
            harga = int(input("masukkan harga : "))
            stock = int(input("masukkan stock barang : "))
            jenis = str(input("masukkan jenis barang : "))

            if nama == "":
                input("Masukkan Data Dengan Benar!!! Tekan ENTER Untuk Kembali.")
                break
            else:
                baru.update({
                    "nama" : nama,
                    "harga" : harga,
                    "stock" : stock,
                    "jenis" : jenis
                            })
                daftar_barang.append(baru)
                simpan_daftar_barang()
                input("Data Berhasil Ditambahkan. Tekan Enter Untuk Kembali. ")
                return
        except ValueError:
            input("Masukkan Data Dengan Benar!! (Harga Harus Berupa Angka).\nTekan ENTER Untuk Kembali.")
            break

def hapus_data_barang():
    while True:
        tampil_data_barang()
        try:
            pil = int(input("Data Ke Berapa Yang Ingin Dihapus : "))
            if pil < 1 or pil > len(daftar_barang):
                input("Pilihan barang tidak valid. Silakan Pilih Nomor Yang Sesuai.\nTekan ENTER Untuk Kembali")
                break
            else:
                daftar_barang.pop(pil-1)
                simpan_daftar_barang()
                input("Data Berhasil Dihapus. Tekan Enter Untuk Kembali. ")
                return
        except ValueError:
            input("Masukkan Data Dengan Benar!! (Pilihan Data Harus Berupa Angka).\nTekan ENTER Untuk Kembali.")
            break

def ubah_data_barang():
    while True:
        tampil_data_barang()
        try:
            pil = int(input("Data Ke Berapa Yang Ingin Diubah : "))
            if pil < 1 or pil > len(daftar_barang):
                input("Pilihan barang Tidak Valid. Silakan Pilih Nomor Yang Sesuai.\nTekan ENTER Untuk Kembali.")
                break
            baru = {}
            nama = str(input("Masukkan Nama : "))
            harga = int(input("Masukkan Harga : "))
            stock = int(input("Masukkan Stock Barang : "))
            jenis = str(input("Masukkan Jenis Barang : "))
            if nama == "":
                input("Masukkan Data Dengan Benar!!! Tekan ENTER Untuk Kembali.")
                break
            else:
                baru.update({
                    "nama" : nama,
                    "harga" : harga,
                    "stock" : stock,
                    "jenis" : jenis
                            })
                daftar_barang[pil-1] = baru
                simpan_daftar_barang()
                input("Data Berhasil Diubah. Tekan Enter Untuk Kembali. ")
                return
        except ValueError:
            input("Masukkan Data Dengan Benar!! (Pilihan Data Dan Harga Harus Berupa Angka).\nTekan ENTER Untuk Kembali.")
            break

def menu_barang(akun):
    while True:
        tampil_data_barang()
        baru = {}
        try:
            nama_user = str(akun["nama"])
            pilih_barang = int(input("Silahkan Pilih Barang : "))
            jumlah = int(input("Silahkan Masukkan Jumlah Barang Yang Akan Dibeli : "))

            if pilih_barang < 1 or pilih_barang > len(daftar_barang):
                input("Nomor barang Tidak Valid. Silakan Pilih Nomor Yang Sesuai.\nTekan ENTER Untuk Kembali.")
                break

            pilih_stock = int(daftar_barang[pilih_barang - 1]["stock"])

            if jumlah < 1 or jumlah > pilih_stock:
                input("Stok barang tidak mencukupi.\nTekan ENTER Untuk Kembali.")
                break

            harga_barang = int(daftar_barang[pilih_barang - 1]["harga"])
            bayar = float(akun["e-money"])
            total = harga_barang * jumlah
            baru.update({
                "nama": daftar_barang[pilih_barang - 1]["nama"],
                "harga":daftar_barang[pilih_barang - 1]["harga"],
                "jumlah":jumlah,
                "jenis":daftar_barang[pilih_barang - 1]["jenis"],
                "total":total
            })
            print("")
            keranjang.append(baru)
            total_harga_belanjaan = tampil_keranjang()
            nambah = input("\nIngin menambah belanjaan? [y/n] : ").lower()
            print("")
            print("")
            if nambah == "y":
                continue
            elif nambah == "n":
                if bayar >= total_harga_belanjaan and total_harga_belanjaan >= 150000 and total_harga_belanjaan < 300000:
                    input("\nSelamat, Karena Anda Berbelanja Sebanyak 150.000\n      Anda Mendapatkan Diskon Sebesar 15%")
                    diskon_awal = 0.15
                    diskon = total_harga_belanjaan * diskon_awal
                    total_akhir = total_harga_belanjaan - diskon
                    saldo_baru = bayar - total_akhir
                    stock_baru = pilih_stock - jumlah
                    akun["e-money"] = saldo_baru
                    daftar_barang[pilih_barang - 1]["stock"] = stock_baru
                    print(keranjang)
                    checkout_diskon(nama_user, total_akhir, diskon_awal)

                elif bayar >= total_harga_belanjaan and total_harga_belanjaan >= 300000:
                    input("\nSelamat, Karena Anda Berbelanja Sebanyak 300.000\n      Anda Mendapatkan Diskon Sebesar 25%")
                    diskon_awal = 0.25
                    diskon = total_harga_belanjaan * diskon_awal
                    total_akhir = total_harga_belanjaan - diskon
                    saldo_baru = bayar - total_akhir
                    stock_baru = pilih_stock - jumlah
                    akun["e-money"] = saldo_baru
                    daftar_barang[pilih_barang - 1]["stock"] = stock_baru
                    print(keranjang)
                    checkout_diskon(nama_user, total_akhir, diskon_awal)

                elif bayar >= total:
                    saldo_baru = bayar - total
                    stock_baru = pilih_stock - jumlah
                    akun["e-money"] = saldo_baru
                    daftar_barang[pilih_barang - 1]["stock"] = stock_baru
                    print(keranjang)
                    checkout(nama_user)

                else:
                    input("\nE-Money Anda Tidak Mencukupi Untuk Membeli Barang Ini")
                    keranjang.clear()
                    break
                simpan_daftar_pelanggan()
                simpan_daftar_barang()
            else:
                input("Pilihan yang anda Masukan tidak valid.") 
                break 
        except ValueError:
            input("Masukkan Dalam Bentuk Angka !!!!\nTekan ENTER Untuk Kembali. ")
            break
        input("Tekan ENTER untuk kembali")
        break

def tampil_keranjang():
    table=PrettyTable()
    table.title = "Keranjang"
    table.field_names = ["Nomor","Nama barang", "Harga", "jumlah", "Jenis", "Total"]
    total_harga = 0
    for i in range(len(keranjang)):
        table.add_row([i+1,keranjang[i]["nama"],f"Rp{keranjang[i]["harga"]}", keranjang[i]["jumlah"], keranjang[i]["jenis"], keranjang[i]["total"]])
        total_harga += keranjang[i]["total"]
    print(total_harga)
    print(table)
    return total_harga

def checkout(akun):
    print("")
    cekot = PrettyTable()
    cekot.title = "Transaksi Berhasil"
    cekot.field_names = ["No", "Nama barang", "Harga", "Jumlah Barang", "Jenis Barang", "Total"]
    total_harga = 0
    for i in range(len(keranjang)):
        cekot.add_row([i+1, keranjang[i]["nama"], keranjang[i]["harga"], keranjang[i]["jumlah"], keranjang[i]["jenis"], keranjang[i]["total"]])
        total_harga += keranjang[i]["total"]
    cekot.add_row(["-------------","-------------","-------------","-------------","-------------", "-------------"])
    cekot.add_row(["Nama User",akun," "," ","Total Keseluruhan", total_harga])
    keranjang.clear()
    print(cekot)

def checkout_diskon(akun, diskon, diskon_awal):
    print("")
    cekot = PrettyTable()
    cekot.title = "Transaksi Berhasil"
    cekot.field_names = ["No", "Nama barang", "Harga", "Jumlah Barang", "Jenis Barang", "Total"]
    total_harga = 0
    for i in range(len(keranjang)):
        cekot.add_row([i+1, keranjang[i]["nama"], keranjang[i]["harga"], keranjang[i]["jumlah"], keranjang[i]["jenis"], keranjang[i]["total"]])
        total_harga += keranjang[i]["total"]
    cekot.add_row(["-------------","-------------","-------------","-------------","-------------", '-------------'])
    cekot.add_row(["Nama User",akun," ", " ", "Total",total_harga])
    cekot.add_row(["-------------","-------------","-------------","-------------","-------------", "-------------"])
    cekot.add_row([" "," ", " ", " ", "Diskon",f"{int(diskon_awal*100)}%"])
    cekot.add_row(["-------------","-------------","-------------","-------------","-------------", "-------------"])
    cekot.add_row([" "," ", " ", " ", "Total Keseluruhan",diskon])
    keranjang.clear()
    print(cekot)
    
def menu_admin(data_admin):
    while True:
        print("")
        print("="*10, "Selamat Datang, " + data_admin["nama"], "="*10)
        print("\nMenu Admin.")
        print("1. Lihat barang")
        print("2. Tambah barang")
        print("3. Hapus barang")
        print("4. Edit Daftar barang")
        print("5. Kembali")
        pil = str(input("Masukkan pilihan : "))

        if pil == "1":
            tampil_data_barang()
            input("Tekan Enter Untuk Kembali. ")
        elif pil == "2":
            tambah_data_barang()
        elif pil == "3":
            hapus_data_barang()
        elif pil == "4":
            ubah_data_barang()
        elif pil == "5":
            break
        else:
            input("Pilihan yang Anda masukan tidak valid. Tekan ENTER Untuk Kembali.")

def menu_pelanggan(data_pengguna,i):
    while True:
        ambil_data_pelanggan_csv()
        saldo_awal = akun_pelanggan[i]["saldo"]

        print("")

        gender = str(data_pengguna["gender"])
        umur = int(data_pengguna["umur"])
        if gender == "L":
            if umur >= 30:
                print("="*10,"Selamat datang, Bapak", data_pengguna["nama"], "="*10)
            elif 19 <= umur <= 29:
                print("="*10,"Selamat datang, Mas", data_pengguna["nama"],"="*10)
            elif 13 <= umur <= 17:
                print("="*10,"Selamat datang, Adek", data_pengguna["nama"],"="*10)
            else:
                print("="*10,"Selamat datang!", data_pengguna["nama"],"="*10)
        elif gender == "P":
            if umur >= 30:
                print("="*10,"Selamat datang, Ibu", data_pengguna["nama"],"="*10)
            elif 19 <= umur <= 29:
                print("="*10,"Selamat datang, Mbak", data_pengguna["nama"],"="*10)
            elif 13 <= umur <= 17:
                print("="*10,"Selamat datang, Adek", data_pengguna["nama"],"="*10)
            else:
                print("="*10,"Selamat datang!", data_pengguna["nama"],"="*10)

        print("\nMenu Pelanggan.")
        print("1. Lihat Saldo")
        print("2. Tambah Saldo")
        print("3. Lihat E-Money")
        print("4. Top-Up E-Money")
        print("5. Pilih barang Yang dibeli")
        print("6. Kembali")
        pil=str(input("Masukkan Pilihan : "))
        if pil=="1":
            pin  = pwinput.pwinput("\nMasukkan PIN Anda : ",mask="*")
            print("")
            if pin == akun_pelanggan[i]["pin"]:
                print("Saldo Anda: Rp" + str(akun_pelanggan[i]["saldo"]))
                input("\nTekan ENTER untuk Kembali Ke Menu.")
            else:
                input("PIN Yang Anda Masukkan Salah!! Tekan ENTER untuk Kembali Ke Menu")
            print("")
        elif pil=="2":
            print("")
            pin  = pwinput.pwinput("Masukkan PIN Anda : ",mask="*")
            if pin == akun_pelanggan[i]["pin"]:
                try:
                    jumlah = int(input("Masukkan Jumlah Saldo Yang Ingin Ditambahkan : "))
                    if jumlah > 0:
                        saldo_akhir = int(saldo_awal) + jumlah
                        akun_pelanggan[i]["saldo"] = saldo_akhir
                        input("Saldo Berhasil Ditambahkan. Tekan ENTER Untuk Kembali.")
                        simpan_daftar_pelanggan()
                    else:
                        input("Jumlah Saldo Harus Positif. Tekan ENTER Untuk Kembali Ke Menu.")
                except ValueError:
                    input("Masukkan Jumlah Saldo Dalam Bentuk Angka. Tekan ENTER Untuk Masukkan Ulang.")
            else:
                input("PIN Yang Anda Masukkan Salah!! Tekan ENTER untuk Kembali Ke Menu")
            print("")
        elif pil=="3":
            pin  = pwinput.pwinput("Masukkan PIN Anda : ",mask="*")
            if pin == akun_pelanggan[i]["pin"]:
                print(f"E-Money Anda: {akun_pelanggan[i]["e-money"]}")
                input("\nTekan ENTER untuk Kembali ke Menu.")
            else:
                input("PIN Yang Anda Masukkan Salah!! Tekan ENTER untuk Kembali ke Menu")
            print("")
        elif pil == "4":
            while True:
                emoney_awal = akun_pelanggan[i].get("e-money")
                print("")
                print("Menu Top-Up")
                print("1. 10000 = Rp13000")
                print("2. 20000 = Rp23000")
                print("3. 50000 = Rp52000")
                print("4. 100000 = Rp101000")
                print("5. 150000 = Rp151000")
                print("6. kembali")
                pilih = input("Silahkan Masukkan Pilihan : ")

                if pilih == "1":
                    if float(saldo_awal) >= 13000:
                        pin  = pwinput.pwinput("Masukkan PIN Anda : ",mask="*")
                        if pin == akun_pelanggan[i]["pin"]:
                            emoney = 10000
                            saldo_emoney_akhir = float(saldo_awal) - 13000
                            emoney_akhir = float(emoney_awal) + float(emoney)
                            akun_pelanggan[i]["saldo"] = saldo_emoney_akhir
                            akun_pelanggan[i]["e-money"] = emoney_akhir
                            simpan_daftar_pelanggan()          
                            input("Top-Up Berhasil. Tekan ENTER Untuk Kembali.")
                        else:
                            input("PIN Yang Anda Masukkan Salah!! Tekan ENTER untuk Kembali Ke Menu")
                    else:
                        input("Saldo yang Anda miliki tidak mencukupi untuk melakukan Top-Up")

                elif pilih == "2":
                    if float(saldo_awal) >= 23000:
                        pin  = pwinput.pwinput("Masukkan PIN Anda : ",mask="*")
                        if pin == akun_pelanggan[i]["pin"]:
                            emoney = 20000
                            saldo_emoney_akhir = float(saldo_awal) - 23000
                            emoney_akhir = float(emoney_awal) + float(emoney)
                            akun_pelanggan[i]["saldo"] = saldo_emoney_akhir
                            akun_pelanggan[i]["e-money"] = emoney_akhir
                            simpan_daftar_pelanggan()          
                            input("Top-Up Berhasil. Tekan ENTER Untuk Kembali.")
                        else:
                            input("PIN Yang Anda Masukkan Salah!! Tekan ENTER untuk Kembali Ke Menu")
                    else:
                        input("Saldo yang Anda miliki tidak mencukupi untuk melakukan Top-Up")

                elif pilih == "3":
                    if float(saldo_awal) >= 52000:
                        pin  = pwinput.pwinput("Masukkan PIN Anda : ",mask="*")
                        if pin == akun_pelanggan[i]["pin"]:
                            emoney = 50000
                            saldo_emoney_akhir = float(saldo_awal) - 52000
                            emoney_akhir = float(emoney_awal) + float(emoney)
                            akun_pelanggan[i]["saldo"] = saldo_emoney_akhir
                            akun_pelanggan[i]["e-money"] = emoney_akhir
                            simpan_daftar_pelanggan()          
                            input("Top-Up Berhasil. Tekan ENTER Untuk Kembali.")
                        else:
                            input("PIN Yang Anda Masukkan Salah!! Tekan ENTER untuk Kembali Ke Menu")
                    else:
                        input("Saldo yang Anda miliki tidak mencukupi untuk melakukan Top-Up")
                elif pilih == "4":
                    if float(saldo_awal) >= 101000:
                        pin  = pwinput.pwinput("Masukkan PIN Anda : ",mask="*")
                        if pin == akun_pelanggan[i]["pin"]:
                            emoney = 100000
                            saldo_emoney_akhir = float(saldo_awal) - 101000
                            emoney_akhir = float(emoney_awal) + float(emoney)
                            akun_pelanggan[i]["saldo"] = saldo_emoney_akhir
                            akun_pelanggan[i]["e-money"] = emoney_akhir
                            simpan_daftar_pelanggan()          
                            input("Top-Up Berhasil. Tekan ENTER Untuk Kembali.")
                        else:
                            input("PIN Yang Anda Masukkan Salah!! Tekan ENTER untuk Kembali Ke Menu")
                    else:
                        input("Saldo yang Anda miliki tidak mencukupi untuk melakukan Top-Up")
                elif pilih == "5":
                    if float(saldo_awal) >= 151000:
                        pin  = pwinput.pwinput("Masukkan PIN Anda : ",mask="*")
                        if pin == akun_pelanggan[i]["pin"]:
                            emoney = 150000
                            saldo_emoney_akhir = float(saldo_awal) - 151000
                            emoney_akhir = float(emoney_awal) + float(emoney)
                            akun_pelanggan[i]["saldo"] = saldo_emoney_akhir
                            akun_pelanggan[i]["e-money"] = emoney_akhir
                            simpan_daftar_pelanggan()          
                            input("Top-Up Berhasil. Tekan ENTER Untuk Kembali.")
                        else:
                            input("PIN Yang Anda Masukkan Salah!! Tekan ENTER untuk Kembali Ke Menu")
                    else:
                        input("Saldo yang Anda miliki tidak mencukupi untuk melakukan Top-Up")

                elif pilih == "6":
                    break
                else:
                    input("Pilihan yang Anda masukkan salah, tekan ENTER untuk kembali")
        elif pil == "5":
            menu_barang(akun_pelanggan[i])
        elif pil == "6":
            break
        else:
            input("Pilihan yang anda masukkan tidak valid, tekan ENTER untuk kembali.")

def login_admin():
    username = str(input("Masukkan Username : "))
    password = str(pwinput.pwinput("Masukkan Sandi : ",mask="*"))
    for i in range(len(akun_admin)):
        if (username == akun_admin[i].get("nama") and password == akun_admin[i].get("sandi")) :
            data_admin = {"nama":akun_admin[i]["nama"]}
            menu_admin(data_admin)
            return
        else:
            continue
    input("Username Atau Password Yang Anda masukkan Salah !! Tekan ENTER Untuk Kembali.")
    print("")

def login_user():
    username = input("Masukkan Username : ")
    password = pwinput.pwinput("Masukkan Sandi : ",mask="*")

    for i in range(len(akun_pelanggan)):
        if username == akun_pelanggan[i].get("nama") and password == akun_pelanggan[i].get("sandi"):

            data_pengguna = {
                "nama": akun_pelanggan[i]["nama"],
                "saldo": akun_pelanggan[i]["saldo"],
                "gender":akun_pelanggan[i]["gender"],
                "umur":akun_pelanggan[i]["umur"]
            }
        
            index_penunjuk_akun = i

            menu_pelanggan(data_pengguna,index_penunjuk_akun)

            return
        else:
            continue
    input("Username Atau Password Yang Anda Masukkan Salah !! Tekan ENTER Untuk Kembali.")
    print("")

def tambah_user():
    while True:
        try:
            baru = {}
            nama = str(input("masukkan nama : ")).strip()
            sandi = int(input("masukkan sandi : "))
            saldo = int(input("masukkan saldo anda : "))
            pin = int(input("masukkan pin : "))
            emoney = 0
            umur = int(input("masukkan umur Anda : "))
            gender = str(input("Masukkan Gender Anda (P/L)")).strip().upper()

            baru.update({
                "nama" : nama,
                "sandi" : sandi,
                "saldo" : saldo,
                "pin" : pin,
                "e-money": emoney,
                "umur": umur,
                "gender": gender,
                        })
            akun_pelanggan.append(baru)
            simpan_daftar_pelanggan()
            input("Pendaftaran Berhasil. Tekan Enter Untuk Kembali. ")
            return
        except ValueError:
            input("Masukkan Data Dengan Benar!! (Sandi Dan Pin Harus Berupa Angka).\nTekan ENTER Untuk Kembali.")
            return
            
while True:
    # if not is_working_hours():
    #     print("Maaf, akses ke menu pelanggan hanya tersedia selama jam kerja (08.00 - 16.00).")
    #     break
    ambil_data_barang_csv()
    ambil_data_pelanggan_csv()
    ambil_data_admin_csv()
    print("="*10,"SELAMAT DATANG DI", "="*10, "\n"," "*12,"TOKO ARTHA","\n")
    print("Menu.")
    print("1. Login Admin")
    print("2. Login Pengguna")
    print("3. Daftar Sebagai Pengguna Baru")
    print("4. Keluar")
    pilihan = str(input("Masukkan Pilihan : "))
    print("")
    if (pilihan=="1"):
        login_admin()
    elif (pilihan=="2"):
        login_user()
    elif (pilihan=="3"):
        tambah_user()
    elif (pilihan=="4"):
        sys.exit()
    else:
        input("Pilihan yang Anda masukan tidak valid.\nSilahkan masukan pilihan (1-4).")
