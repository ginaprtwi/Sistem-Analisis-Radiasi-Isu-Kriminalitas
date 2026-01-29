import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Isu & Wilayah Dominan")
st.text("Visualisasi ini membantu menentukan prioritas isu kriminal dan wilayah yang perlu dipantau berdasarkan intensitas pemberitaann kriminalitas Detik.com")
df = pd.read_excel("fix_data.xlsx")

#filter tahun
df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")
list_tahun = sorted(df["tahun"].dropna().astype(int).unique())

with st.container(border=True):
    tahun_selected = st.pills(
        "Pilih Tahun",
        options=list_tahun,
        default=list_tahun,
        selection_mode="multi",
    )

#biar ga error kalau ga pilih tahun
if not tahun_selected:
    dftahun = df.iloc[0:0]  # dataframe kosong
    label_waktu = "Tidak ada tahun dipilih"
    st.warning("Silakan pilih minimal satu tahun untuk menampilkan data.", icon="⚠️")
else:
    dftahun = df[df["tahun"].isin(tahun_selected)]
    if len(tahun_selected) == 1:
        label_waktu = f"Tahun {tahun_selected[0]}"
    else:
        label_waktu = f"Periode {min(tahun_selected)}–{max(tahun_selected)}"

#total
total_kasus = len(dftahun)

grouped_jenis = (dftahun.groupby("jenis_kriminal")["judul"].count().sort_values(ascending=False)
    if not dftahun.empty else pd.Series(dtype=int))
grouped_prov = (
    dftahun.groupby("provinsi")["judul"].count().sort_values(ascending=False)
    if not dftahun.empty else pd.Series(dtype=int))

kriminal_dominan = grouped_jenis.idxmax() if not grouped_jenis.empty else "-"
top_prov_nama = grouped_prov.idxmax() if not grouped_prov.empty else "-"
top_prov_val = grouped_prov.max() if not grouped_prov.empty else 0
bottom_prov_nama = grouped_prov.idxmin() if not grouped_prov.empty else "-"




st.subheader(f"Grafik Isu Kriminal ({label_waktu})")

#bar isu kriminal
with st.container(border=True):
    col1, col2= st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(10, 7))

        if not dftahun.empty:
            df_pivot = dftahun.pivot_table(
                index="jenis_kriminal",
                columns="tahun",
                values="judul",
                aggfunc="count"
            ).fillna(0)

            df_pivot.plot(
                kind="bar",
                stacked=True,
                ax=ax1,
                edgecolor="black"
            )

        ax1.set_title("Distribusi Jenis Kriminal")
        ax1.set_ylabel("Jumlah Isu")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig1)

#line prov top 10
    with col2:
        fig2, ax2 = plt.subplots(figsize=(10, 7))

        if not grouped_prov.empty:
            top_10_p = grouped_prov.head(10).index
            df_top = dftahun[dftahun["provinsi"].isin(top_10_p)]

            df_pivot_prov = df_top.pivot_table(
                index="provinsi",
                columns="tahun",
                values="judul",
                aggfunc="count"
            ).fillna(0)

            for col in df_pivot_prov.columns:
                ax2.plot(
                    df_pivot_prov.index,
                    df_pivot_prov[col],
                    marker="o",
                    label=str(col)
                )   

            ax2.legend(title="Tahun")

            ax2.set_title("Top 10 Wilayah dengan Isu Kriminal Terbanyak")
            ax2.set_ylabel("Jumlah Isu")
            plt.xticks(rotation=45, ha="right")
            ax2.grid(True, linestyle="--", alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig2)
            
# insight isu dan kota
with st.container(border=True):
    st.markdown(f"### Insight ({label_waktu})")
    
    if total_kasus == 0:
        st.markdown(
            "Tidak terdapat data yang dapat dianalisis karena **belum ada tahun yang dipilih**."
        )
    else:
        st.markdown(f"""
Berdasarkan hasil analisis pada **{label_waktu}**, tercatat **{total_kasus} isu kriminalitas** yang diberitakan oleh Detik.com.  s

🔹 **Jenis kriminal dominan:** {kriminal_dominan} 

🔹 **Wilayah paling sering diberitakan:** {top_prov_nama} ({top_prov_val} isu) 

🔹 **Wilayah dengan intensitas terendah:** {bottom_prov_nama}  
""")
