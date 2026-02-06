import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Dashboard")
st.text("Ringkasan Pemberitaan Kriminalitas: Prioritas Isu, Wilayah, dan Sumber Media (2024–2025) berdasarkan media online Detik.com")

df = pd.read_excel("data/fix_data.xlsx")

jenis_terbanyak = df["jenis_kriminal"].value_counts().idxmax().capitalize()
prov_terbanyak = df["provinsi"].value_counts().idxmax()
sumber_teraktif = df["sumber"].value_counts().idxmax()
sentimen_dominan = df["sentimen"].value_counts().idxmax()
#urutin sesuai tgl
df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")

#rekomendasi
jenis_terbanyak = df["jenis_kriminal"].value_counts().idxmax()
topik = df[df["jenis_kriminal"] == jenis_terbanyak]
topik = topik.sort_values("tanggal", ascending=False)
rekomendasi = topik.head(3)
jenis_terbanyak = df["jenis_kriminal"].value_counts().idxmax().capitalize()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    with st.container(border=True):
        st.caption("Jumlah Berita")
        st.markdown(f"**{len(df)}**")

with col2:
    with st.container(border=True):
        st.caption("Isu Dominan")
        st.markdown(f"**{jenis_terbanyak}**")

with col3:
    with st.container(border=True):
        st.caption("Wilayah Dominan")
        st.markdown(f"**{prov_terbanyak}**")

with col4:
    with st.container(border=True):
        st.caption("Sumber Dominan")
        st.markdown(f"**{sumber_teraktif}**")
with col5:
    with st.container(border=True):
        st.caption("Sentimen Dominan")
        st.markdown(f"**{sentimen_dominan}**")



with st.container(border=True):
    st.text("Rekomendasi Berita Berdasarkan Isu Dominan: Menampilkan berita terbaru terkait isu kriminalitas prioritas")

    if rekomendasi.empty:
        st.info("Tidak ada rekomendasi berita untuk ditampilkan.")
    else:
        for _, row in rekomendasi.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])  
            with col1:
                st.markdown(f"**{row['judul'].title()}**")
                st.caption(f"{row['tanggal'].strftime('%d-%m-%Y')} | {row['sumber']}")

            with col2:
                st.markdown(f"[Baca selengkapnya]({row['link']})")

        