import pymysql
from datetime import datetime

waktu = datetime.now()

db = pymysql.connect(host="localhost", port=3306,
                     user="root", passwd="", database="sistembengkel")
cursor = db.cursor()

queryharga = (f'''UPDATE `transaksi` SET `waktu_pembayaran` = '{waktu}' WHERE id_transaksi = 2;''')
cursor.execute(queryharga)
querycustomer = (f'''UPDATE `customer` SET `status` = 'selesai', `tanggal_selesai` = '{waktu}' WHERE id_customer = {idnya}''')
cursor.execute(querycustomer)

db.commit()

# queryharga = (f'''SELECT customer.Nama, customer.tanggal_masuk, customer.tanggal_selesai, customer.kerusakan, customer.merk_motor, customer.tipe_motor, sparepart.nama_sparepart, sparepart.harga_sparepart, transaksi.id_transaksi, transaksi.harga, transaksi.waktu_pembayaran, customer.kembalian FROM transaksi JOIN sparepart ON transaksi.id_sparepart = sparepart.id_sparepart JOIN customer ON transaksi.id_customer = customer.id_customer WHERE transaksi.id_customer = 1;''')

# cursor.execute(queryharga)
# i = cursor.fetchall()
# motor = i[0][4], i[0][5]
# def loop():
#     jumlahTotal  = 0
#     count = 0
#     for a in i :
#         count += 1
#         print("Sparepart Diganti   : ", a[6])
#         jumlahTotal += int(a[7])


#     print("Jumlah Total : ",jumlahTotal)

#     print("Uang Kembalian : ", i[0][11])
#     print("\n############### ############### ###############")


# print(f'''\n
# ############### STRUK PEMBAYARAN ###############
#         ###### BENGKEL JAYABAYA ######
#         Jl. RingRoad Utara No 28
#                 Yogyakarta
            
#             {i[0][10]}
# Customer ID         : {i[0][8]}
# Nama Customer       : {i[0][0]}
# Tanggal Masuk       : {i[0][1]}
# Tanggal Keluar      : {i[0][2]}
# Kerusakan           : {i[0][3]}
# Tipe Motor          : {i[0][4] +" "+ i[0][5]}
# Tipe Kerusakan      : {i[0][3]}
# ''')



# loop()