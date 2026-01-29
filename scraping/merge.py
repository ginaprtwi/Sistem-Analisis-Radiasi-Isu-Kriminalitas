import pandas as pd
import os

# Folder tempat semua Excel
folder_path = "scraping/detik.com" 

# List semua file Excel di folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]

all_df = []

for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path, engine="openpyxl")
    all_df.append(df)

# Merge semua DataFrame
merged_df = pd.concat(all_df, ignore_index=True)

# Simpan ke Excel baru
merged_file = os.path.join(folder_path, "raw_data.xlsx")
merged_df.to_excel(merged_file, index=False, engine="openpyxl")

print(f"✅ Semua file berhasil digabung. Tersimpan di: {merged_file}")
print(f"Total baris: {len(merged_df)}")
