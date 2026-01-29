import pandas as pd
df = pd.read_excel("fix_data.xlsx")

print(df["jenis_kriminal"].value_counts())