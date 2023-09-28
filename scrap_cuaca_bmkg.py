import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# URL yang akan di-scrap
url = 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca.bmkg?Kota=Wates&AreaID=501188&Prov=6'
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36'
}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')

# mencari semua elemen cuaca dalam elemen hari
hari = soup.findAll('div', 'prakicu-kabkota tab-v1 margin-bottom-30')

datas = []
for days in hari:
    # Mengambil teks dari elemen <a> dalam elemen <li> dalam elemen <ul> untuk nama hari dan tanggal beserta bulan
    day_elements = days.find('ul', class_='nav nav-tabs').find_all('li')
    for li_element in day_elements:
        a_element = li_element.find('a')
        if a_element:
            day_text = a_element.text

            # menentukan ID tab yang sesuai dengan tanggal
            tab_id = a_element.get('href').split('#')[1]

            # mengambil semua elemen cuaca dalam elemen tab
            waktu = days.find('div', {'id': tab_id}).findAll('div', 'cuaca-flex-child')
            for item in waktu:
                waktu = item.find('h2', class_='kota').text
                cuaca = item.find('div', class_='kiri').p.text
                suhu = item.find('h2', class_='heading-md').text
                kelembaban = item.find('div', class_='kanan').p.text
                angin = item.find('div', class_='kanan').find_all('p')[1].text
                datas.append([day_text, waktu, cuaca, suhu, kelembaban, angin])

# Mendefinisikan nama file CSV
nama_file_csv = 'data_perkiraan_cuaca_bmkg.csv'

# Menulis data ke dalam file CSV
with open(nama_file_csv, 'w', newline='') as file_csv:
    writer = csv.writer(file_csv)
    title = ['Perkiraan Cuaca di Kabupaten Kulon Progo menurut BMKG']
    head = ['Hari & Tanggal', 'Waktu', 'Cuaca', 'Suhu', 'Kelembaban Udara', 'Kecepatan & Arah Angin']
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%A, %d %B %Y %H:%M:%S')
    writer.writerow(title)
    writer.writerow(head)
    for d in datas:
        writer.writerow(d)
    writer.writerow(['Diakses pada ' + formatted_datetime])
