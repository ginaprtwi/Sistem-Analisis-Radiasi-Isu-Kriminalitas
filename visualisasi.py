import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide") # Opsional: Agar tampilan lebih lebar
st.title("Visualisasi Data Kriminal")

# =======================
# LOAD DATA
# =======================
@st.cache_data # Menggunakan cache agar load data lebih cepat
def load_data():
    df = pd.read_excel("fix_dataa.xlsx")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    df = df.rename(columns={"nis_kriminal": "jenis_kriminal"})
    return df

df = load_data()

# =======================
# FILTER TAHUN (MODIFIKASI)
# =======================
# Menambahkan opsi "Semua Tahun" di awal list
tahun_list = ["Semua Tahun"] + sorted(df["tahun"].unique().tolist())
tahun_pilih = st.selectbox("Pilih Tahun", tahun_list)

# Logika Filter
if tahun_pilih == "Semua Tahun":
    df_filtered = df
    label_waktu = "Semua Tahun"
else:
    df_filtered = df[df["tahun"] == tahun_pilih]
    label_waktu = f"Tahun {tahun_pilih}"

# =======================
# GROUPING
# =======================
grouped_jenis = df_filtered.groupby("jenis_kriminal")["judul"].count().sort_values(ascending=False)
grouped_kota = df_filtered.groupby("kota")["judul"].count().sort_values(ascending=False)
grouped_sumber = df_filtered.groupby("sumber")["judul"].count().sort_values(ascending=False)

# Ambil TOP 10 kota agar grafik jelas
top_kota = grouped_kota.head(10)

# =======================
# TAMPILAN
# =======================
col1, col2 = st.columns(2)

# -------- BAR JENIS KRIMINAL --------
with col1:
    st.subheader(f"Jenis Kriminal ({label_waktu})")
    fig1, ax1 = plt.subplots(figsize=(8,6))
    ax1.bar(grouped_jenis.index, grouped_jenis.values, color="orange")
    ax1.set_xlabel("Jenis Kriminal")
    ax1.set_ylabel("Jumlah Isu")
    ax1.set_title(f"Jumlah Isu Berdasarkan Jenis Kriminal - {label_waktu}")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig1)

# -------- GRAFIK GARIS KOTA --------
with col2:
    st.subheader(f"Kota Terbanyak ({label_waktu})")
    fig2, ax2 = plt.subplots(figsize=(8,6))
    ax2.plot(top_kota.index, top_kota.values, marker="o", color="blue", linestyle="-")
    ax2.set_xlabel("Kota")
    ax2.set_ylabel("Jumlah Isu")
    ax2.set_title(f"Top 10 Kota Kriminal - {label_waktu}")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig2)

# -------- PIE CHART SUMBER BERITA --------
st.markdown("---")
st.subheader(f"Distribusi Sumber Berita ({label_waktu})")

# Ambil TOP 10 agar pie chart jelas
top_sumber = grouped_sumber.head(10)
lainnya_val = grouped_sumber.iloc[10:].sum() if len(grouped_sumber) > 10 else 0

if lainnya_val > 0:
    # Buat Series baru untuk "Lainnya"
    s_lainnya = pd.Series({"Lainnya": lainnya_val})
    top_sumber = pd.concat([top_sumber, s_lainnya])

fig3, ax3 = plt.subplots(figsize=(7,7))
ax3.pie(
    top_sumber.values, 
    labels=top_sumber.index, 
    autopct="%1.1f%%", 
    startangle=140,
    colors=plt.cm.Paired(np.linspace(0, 1, len(top_sumber)))
)
ax3.set_title(f"Proporsi Sumber Berita - {label_waktu}")
st.pyplot(fig3)