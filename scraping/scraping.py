import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# ================= INPUT =================
query = input("Masukan kata kunci kriminalitas: ")
halaman_awal = int(input("Masukan halaman awal: "))
halaman_akhir = int(input("Masukan halaman akhir: "))
nama_file = input("Nama file Excel (tanpa .xlsx): ")

folder_path = os.path.join("scraping", "detik.com")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

all_data = []

# ================= SCRAPING =================
for p in range(halaman_awal, halaman_akhir + 1):
    print(f"Scraping page {p}...")
    url = f"https://www.detik.com/search/searchall?query={query}&result_type=latest&page={p}"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"   > Gagal page {p}: {e}")
        continue

    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup.find_all("article")

    if not articles:
        print("   > Tidak ada artikel, stop.")
        break

    for article in articles:
        # Judul + Link
        title_tag = article.select_one(".media__title a")
        judul = title_tag.get_text(strip=True) if title_tag else "-"
        link = title_tag["href"] if title_tag else "-"

        # Tanggal
        date_div = article.select_one(".media__date span")
        tanggal = date_div["title"] if date_div and date_div.has_attr("title") else "-"

        # Sumber
        sumber_tag = article.select_one(".media__subtitle")
        sumber = sumber_tag.get_text(strip=True) if sumber_tag else "-"

        if judul != "-" and link != "-":
            all_data.append({
                "judul": judul,
                "link": link,
                "tanggal": tanggal,
                "sumber": sumber
            })

    time.sleep(5)  

file_path = os.path.join(folder_path, f"{nama_file}.xlsx")
df = pd.DataFrame(all_data)
df.to_excel(file_path, index=False, engine="openpyxl")

print(f"Data tersimpan di {nama_file}.xlsx")

