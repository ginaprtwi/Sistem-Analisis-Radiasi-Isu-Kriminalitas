import pandas as pd
import streamlit as st

df = pd.read_excel("fix_dataa.xlsx")

st.title("Data Berita")
st.dataframe(df)
