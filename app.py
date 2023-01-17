import pymysql
from datetime import datetime


# database db
waktu = datetime.now()
db = pymysql.connect(host="localhost", port=3306, user="root", passwd="", database="sistembengkel")
cursor = db.cursor()

def menu():
    print("\n","*"*15,"ADMIN BENGKEL","*"*15)
    print("\n","*"*10,"JAYABAYA","*"*10)
    print("1.   Customer Baru ")
    print("2.   Pembayaran")
    print("3.   Cetak Struk")
    print("4.   Input SparePart ")
    print("5.   Input Transaksi")
    print("6.   Log Out \n")
    print("*"*31, "\n")
    pilihan = int(input("Masukan Pilihan Anda : "))
    return pilihan

def sparepart():

    id_sparepart = int(input("\nMasukan ID Sparepart : "))
    nama_brang = str(input("Masukan Nama Sparepart : "))
    stok_barang = int(input("Masukan Jumlah Sparepart : "))
    harga_barang = int(input("Masukan Harga Sparepart : "))

    quer = (f'''INSERT INTO `sparepart`(`id_sparepart`, `nama_sparepart`, `stok_sparepart`, `harga_sparepart`) VALUES ('{id_sparepart}','{nama_brang}','{stok_barang}','{harga_barang}')''')
    cursor.execute(quer)
    db.commit()

    print("SparePart Berhasil di Tambahkan ! ")
    menu()

def main():

    pilihan = menu()
    
    if pilihan == 1 :
        return inputDataCustom()
    elif pilihan == 2 :
        return pembayaran()
    elif pilihan == 3 :
        return cetakStruk()
    elif pilihan == 4 :
        return sparepart()
    elif pilihan == 5 :
        return transaksi()
    elif pilihan == 6 :
        return login()

def pembayaran():

    id_pelanggan = int(input("\nMasukan Id Pelanggan : "))
    query = (f'''SELECT `id_transaksi` FROM `transaksi` WHERE id_customer = {id_pelanggan};''')
    cursor.execute(query)
    result = cursor.fetchone()

    if result :
        Bayar(id_pelanggan)
    else:
        print("\nData Is Not Found !")
        pembayaran()

def cetakStruk():
    idnya = int(input("Masukan id Pelanggan : "))
    query = (f'''SELECT customer.Nama, customer.tanggal_masuk, customer.tanggal_selesai, customer.kerusakan, customer.merk_motor, customer.tipe_motor, sparepart.nama_sparepart, sparepart.harga_sparepart, transaksi.id_transaksi, transaksi.harga, transaksi.waktu_pembayaran, customer.kembalian FROM transaksi JOIN sparepart ON transaksi.id_sparepart = sparepart.id_sparepart JOIN customer ON transaksi.id_customer = customer.id_customer WHERE transaksi.id_customer = {idnya};''')

    cursor.execute(query)
    i = cursor.fetchall()
    def loop():
        jumlahTotal  = 0
        count = 0
        for a in i :
            count += 1
            print("Sparepart Diganti   : ", a[6])
            jumlahTotal += int(a[7])
        print("Jumlah Total : ",jumlahTotal)
        print("Uang Kembalian : ", i[0][11])
        print("\n############### ############### ###############")

    print(f'''\n
    ############### STRUK PEMBAYARAN ###############
            ###### BENGKEL JAYABAYA ######
            Jl. RingRoad Utara No 28
                    Yogyakarta
                
                {i[0][10]}
    Customer ID         : {i[0][8]}
    Nama Customer       : {i[0][0]}
    Tanggal Masuk       : {i[0][1]}
    Tanggal Keluar      : {i[0][2]}
    Kerusakan           : {i[0][3]}
    Tipe Motor          : {i[0][4] +" "+ i[0][5]}
    Tipe Kerusakan      : {i[0][3]}
    ''')
    loop()

def login():
    print("\n Silahkan Login Sebagai Admin\n")
    query = ("SELECT * FROM admin WHERE username = %s AND password = %s")

    # Define the parameters
    username = input("Username : ")
    password = input("Password : ")
    params = (username, password)

    # Menjalankan query
    cursor.execute(query, params)

    # Menampilkan 
    result = cursor.fetchone()

    # Check Admin
    if result:
        main()
    else:
        return print("Gagal Login")

def inputDataCustom():

    print("\n","*"*15,"INPUT PELANGGAN BARU","*"*15)
    nama = input("Masukan Nama Pelanggan : ")
    merkMotor = input("Masukan Brand Motor : ")
    tipeMotor = input("Masukan Tipe Motor : ")
    jenisMotor = input("Masukan Jenis Motor : ")
    tanggal_masuk = waktu
    kerusakan = input("Masukan jenis kerusakan motor : ")
    status = input("Masukan status motor : ")

    query = (f'''INSERT INTO `customer`( `Nama`, `kerusakan`, `tanggal_masuk`, `tanggal_selesai`, `status`, `merk_motor`, `jenis_motor`, `tipe_motor`) VALUES ('{nama}','{kerusakan}','{tanggal_masuk}','','{status}','{merkMotor}','{jenisMotor}','{tipeMotor}')''')
    cursor.execute(query)
    db.commit()
    print("\nData Berhasil Di Inputkan !\n")

def Bayar(id_pelanggan):

    idnya = id_pelanggan

    queryharga = (f'''SELECT customer.Nama, customer.tanggal_masuk, customer.tanggal_selesai, customer.kerusakan, customer.merk_motor, customer.tipe_motor, sparepart.nama_sparepart, sparepart.harga_sparepart, transaksi.id_transaksi, transaksi.harga, transaksi.waktu_pembayaran, sparepart.id_sparepart  FROM transaksi JOIN sparepart ON transaksi.id_sparepart = sparepart.id_sparepart JOIN customer ON transaksi.id_customer = customer.id_customer WHERE transaksi.id_customer = {idnya};''')

    cursor.execute(queryharga)
    i = cursor.fetchall()
    motor = i[0][4], i[0][5]
    def loop():
        jumlahTotal  = 0
        stok = 0
        for a in i :
            print("Sparepart Diganti   : ", a[6])
            jumlahTotal += int(a[7])
            stok += 1

            # db.commit()
        print("\nJumlah Total        : ", jumlahTotal, "\n")

        nominalbayar = int(input("Masukan Jumlah Bayar : "))
        kembalian = abs(nominalbayar - jumlahTotal)

        sparepartStok = f'''SELECT `stok_sparepart` FROM `sparepart` WHERE id_sparepart={a[11]} '''
        cursor.execute(sparepartStok)
        stk = cursor.fetchall()[0][0]

        totalStok = stk - stok
        quer = (f'''UPDATE `sparepart` SET `stok_sparepart` ={totalStok} WHERE id_sparepart={a[11]} ''')
        cursor.execute(quer)
        quer = (f'''UPDATE `customer` SET `kembalian` ={kembalian} WHERE id_customer={idnya} ''')
        cursor.execute(quer)
        queryharga = (f'''UPDATE `transaksi` SET `waktu_pembayaran` = '{waktu}' WHERE id_transaksi = {id_pelanggan};''')
        cursor.execute(queryharga)
        querycustomer = (f'''UPDATE `customer` SET `status` = 'selesai', `tanggal_selesai` = '{waktu}' WHERE id_customer = {id_pelanggan}''')
        cursor.execute(querycustomer)
   
        db.commit()

        print("Uang Kembali : ",kembalian)
        print("\n############### ############### ###############")
        main()
    print(f'''\n
############### PEMBAYARAN ###############

Nama Customer       : {i[0][0]}
Tanggal Masuk       : {i[0][1]}
Kerusakan           : {i[0][3]}
Tipe Motor          : {i[0][4] +" "+ i[0][5]}
Tipe Kerusakan      : {i[0][3]}
''')
    loop()

def transaksi():

    id_pelanggan = int(input("Masukan Id Pelanggan : "))
    id_sparepart = int(input("Masukan ID SparePart : "))
    into = (f'''INSERT INTO `transaksi`( `id_sparepart`,`id_transaksi`,`id_customer`) VALUES ({id_sparepart},{id_pelanggan},{id_pelanggan})''')

    cursor.execute(into)
    db.commit()

    print("Kebutuhan Pelanggan Berhasil Di Tambahkan ! \n")
    main()
login()