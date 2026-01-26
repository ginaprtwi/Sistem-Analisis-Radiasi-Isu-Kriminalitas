import pandas as pd
import re #buat baca pola 20xx krn klo langsung ubah ke date time ga kebaca semua data nya

df = pd.read_excel("raw_data.xlsx")

#cek duplikat
df = df.drop_duplicates(subset=["judul", "link"])

#biar sama format judulnya
df["judul"] = df["judul"].str.lower()

#hapus hari dan jam, sisain tgl
def get_tanggal_tahun(x):
    # Step 1: kalau sudah datetime, langsung ambil
    if isinstance(x, pd.Timestamp):
        return x, x.year
    try:
        # bersihkan string
        s = str(x).replace("\xa0"," ").replace("WIB","").strip()
        dt = pd.to_datetime(s, dayfirst=True, errors="coerce")
        if pd.notna(dt):
            return dt, dt.year
        else:
            # backup: ambil 4 digit 20xx dari string asli, kalau tahun ga kebaca
            match = re.search(r"20\d{2}", s)
            if match:
                year = int(match.group())
                dt_backup = pd.Timestamp(f"{year}-01-01")
                return dt_backup, year
            else:
                return pd.NaT, 0 #pd.Nat buat nandain tgl yg ga valid biar ga error
    except:
        return pd.NaT, 0 #klo ga ketemu 0

# masukin fungsi ke data frame
df[["tanggal_parsed","tahun"]] = df["tanggal"].apply(get_tanggal_tahun).apply(pd.Series)

# buat kolom tanggal string
df["tanggal"] = df["tanggal_parsed"].dt.strftime("%Y-%m-%d")

# hapus kolom sementara
df = df.drop(columns=["tanggal_parsed"])

# kata kunci kriminal
kata_kunci = {
    "pembunuhan": [
        "bunuh","dibunuh","pembunuhan",
        "tewas","mayat","meninggal",
        "habisi","menghabisi","tragis","tewas mengenaskan"
    ],

    "penculikan": [
        "culik", "penculikan", "diculik", "penyekapan", "disekap"
    ],

    "judi online": [
        "judi", "judol", "perjudian"
    ],

    "kekerasan": [
        "aniaya","dianiaya","penganiayaan",
        "keroyok","pengeroyokan","dikeroyok",
        "pukul","pemukulan","bacok","pembacokan",
        "tusuk","penusukan","tembak","penembakan",
        "kdrt","aniaya istri","aniaya suami",
        "aniaya anak", "kekerasan","pengancaman","ancam",
        "intimidasi","brutal"
    ],

    "pencurian": [
        "curi","pencurian","maling",
        "jambret","rampok","perampokan",
        "begal","bajing loncat", "dirampas",
        "merampas","scam","penipuan","phising", 
        "pinjol", "tppu", "bandit", "data fiktif", 
        "menipu", "tertipu","curanmor", "raib", "copet", 
        "perampas", "pembobolan"
    ],

    "narkoba": [
        "narkoba","sabu","ganja","ekstasi",
        "pil koplo","obat terlarang","tembakau"
    ],

    "pemerkosaan": [
        "perkosa","pemerkosaan",
        "cabul","pencabulan",
        "asusila","pelecehan", "memerkosa"
    ]
}

#kata kunci framing media
kamus_sentimen = {
    "positif": [
        "berhasil ditangkap",
        "ditangkap",
        "tersangka diamankan",
        "tertangkap"
    ],
    "negatif": [
        "kabur",
        "tidak tertangkap",
        "menghilang",
        "merajalela",
        "menyerang",
        "korupsi",
        "kriminal",
        "razia"
    ]
}
#kata kunci yg nanti nya bakal di drop
kata_drop = [
    "sosialisasi","edukasi","kampanye",
    "kunjungan","peresmian","rapat","apel",
    "pengamanan","siaga","lalu lintas","kecelakaan",
    "banjir","longsor", "tiket konser", "lowongan kerja", "internasional"
]

sumber_drop = [
    "detikfood", "detikHot", "detikFinance", "detikInet"
]

#kata kunci kota
kotaxprov = {

    # =====================
    # DKI Jakarta
    # =====================
    "jakarta": "Jakarta Raya",
    "dki": "Jakarta Raya",
    "jakpus": "Jakarta Raya",
    "jaksel": "Jakarta Raya",
    "jakbar": "Jakarta Raya",
    "jaktim": "Jakarta Raya",
    "jakut": "Jakarta Raya",
    "kep seribu": "Jakarta Raya",
    "kepulauan seribu": "Jakarta Raya",

    # =====================
    # Jawa Barat
    # =====================
    "jabar": "Jawa Barat",
    "bandung": "Jawa Barat",
    "kab bandung": "Jawa Barat",
    "bandung barat": "Jawa Barat",
    "bekasi": "Jawa Barat",
    "kab bekasi": "Jawa Barat",
    "bogor": "Jawa Barat",
    "kab bogor": "Jawa Barat",
    "depok": "Jawa Barat",
    "cimahi": "Jawa Barat",
    "garut": "Jawa Barat",
    "tasik": "Jawa Barat",
    "tasikmalaya": "Jawa Barat",
    "cirebon": "Jawa Barat",
    "kab cirebon": "Jawa Barat",
    "sukabumi": "Jawa Barat",
    "sumedang": "Jawa Barat",
    "subang": "Jawa Barat",
    "karawang": "Jawa Barat",
    "purwakarta": "Jawa Barat",
    "indramayu": "Jawa Barat",
    "majalengka": "Jawa Barat",
    "ciamis": "Jawa Barat",

    # =====================
    # Banten
    # =====================
    "banten": "Banten",
    "tangerang": "Banten",
    "kab tangerang": "Banten",
    "tangsel": "Banten",
    "tangerang selatan": "Banten",
    "serang": "Banten",
    "cilegon": "Banten",
    "lebak": "Banten",
    "pandeglang": "Banten",

    # =====================
    # Jawa Tengah
    # =====================
    "jateng": "Jawa Tengah",
    "semarang": "Jawa Tengah",
    "solo": "Jawa Tengah",
    "surakarta": "Jawa Tengah",
    "purwokerto": "Jawa Tengah",
    "cilacap": "Jawa Tengah",
    "pekalongan": "Jawa Tengah",
    "tegal": "Jawa Tengah",
    "magelang": "Jawa Tengah",
    "salatiga": "Jawa Tengah",
    "kudus": "Jawa Tengah",
    "jepara": "Jawa Tengah",
    "pati": "Jawa Tengah",
    "demak": "Jawa Tengah",
    "klaten": "Jawa Tengah",
    "boyolali": "Jawa Tengah",
    "wonogiri": "Jawa Tengah",

    # =====================
    # DI Yogyakarta
    # =====================
    "diy": "DI Yogyakarta",
    "jogja": "DI Yogyakarta",
    "yogyakarta": "DI Yogyakarta",
    "sleman": "DI Yogyakarta",
    "bantul": "DI Yogyakarta",
    "kulon progo": "DI Yogyakarta",
    "gunungkidul": "DI Yogyakarta",

    # =====================
    # Jawa Timur
    # =====================
    "jatim": "Jawa Timur",
    "surabaya": "Jawa Timur",
    "sby": "Jawa Timur",
    "malang": "Jawa Timur",
    "kab malang": "Jawa Timur",
    "sidoarjo": "Jawa Timur",
    "gresik": "Jawa Timur",
    "mojokerto": "Jawa Timur",
    "kediri": "Jawa Timur",
    "blitar": "Jawa Timur",
    "pasuruan": "Jawa Timur",
    "probolinggo": "Jawa Timur",
    "jember": "Jawa Timur",
    "banyuwangi": "Jawa Timur",
    "madiun": "Jawa Timur",
    "ponorogo": "Jawa Timur",
    "tuban": "Jawa Timur",
    "lamongan": "Jawa Timur",

    # =====================
    # Sumatera (umum media)
    # =====================
    "sumut": "Sumatera Utara",
    "medan": "Sumatera Utara",
    "binjai": "Sumatera Utara",
    "siantar": "Sumatera Utara",

    "sumsel": "Sumatera Selatan",
    "palembang": "Sumatera Selatan",

    "sumbar": "Sumatera Barat",
    "padang": "Sumatera Barat",
    "bukittinggi": "Sumatera Barat",

    "riau": "Riau",
    "pekanbaru": "Riau",
    "dumai": "Riau",

    "kepri": "Kepulauan Riau",
    "batam": "Kepulauan Riau",
    "tanjungpinang": "Kepulauan Riau",

    "aceh": "Aceh",
    "banda aceh": "Aceh",
    "lhokseumawe": "Aceh",

    "lampung": "Lampung",
    "bandar lampung": "Lampung",

    # =====================
    # Kalimantan
    # =====================
    "kaltim": "Kalimantan Timur",
    "balikpapan": "Kalimantan Timur",
    "samarinda": "Kalimantan Timur",

    "kalsel": "Kalimantan Selatan",
    "banjarmasin": "Kalimantan Selatan",

    "kalbar": "Kalimantan Barat",
    "pontianak": "Kalimantan Barat",

    "kalteng": "Kalimantan Tengah",
    "palangkaraya": "Kalimantan Tengah",

    "kalut": "Kalimantan Utara",
    "tarakan": "Kalimantan Utara",

    # =====================
    # Sulawesi
    # =====================
    "sulsel": "Sulawesi Selatan",
    "makassar": "Sulawesi Selatan",
    "gowa": "Sulawesi Selatan",

    "sulteng": "Sulawesi Tengah",
    "palu": "Sulawesi Tengah",

    "sulut": "Sulawesi Utara",
    "manado": "Sulawesi Utara",

    "sultra": "Sulawesi Tenggara",
    "kendari": "Sulawesi Tenggara",

    # =====================
    # Bali & Nusa Tenggara
    # =====================
    "bali": "Bali",
    "denpasar": "Bali",
    "badung": "Bali",

    "ntb": "Nusa Tenggara Barat",
    "mataram": "Nusa Tenggara Barat",

    "ntt": "Nusa Tenggara Timur",
    "kupang": "Nusa Tenggara Timur",

    # =====================
    # Papua
    # =====================
    "papua": "Papua",
    "jayapura": "Papua",
    "merauke": "Papua",

    # =====================
# Jambi
# =====================
"jambi": "Jambi",
"prov jambi": "Jambi",
"kota jambi": "Jambi",
"muaro jambi": "Jambi",
"muara jambi": "Jambi",
"batanghari": "Jambi",
"tebo": "Jambi",
"bungo": "Jambi",
"tanjab barat": "Jambi",
"tanjab timur": "Jambi",
"tanjung jabung barat": "Jambi",
"tanjung jabung timur": "Jambi",
"sarolangun": "Jambi",
"merangin": "Jambi",
"kerinci": "Jambi",
"sungai penuh": "Jambi",

}


#buat kolom baru 
df["kota"] = df["judul"].apply(
    lambda x: next((k for k in kotaxprov.keys() if k in x), "lainnya")
)

df["provinsi"] = df["judul"].apply(
    lambda x: next((v for k, v in kotaxprov.items() if k in x), "Lainnya")
)

df["jenis_kriminal"] = df["judul"].apply(
    lambda x: next((key for key, kws in kata_kunci.items() if any(kw in x for kw in kws)), "lainnya")
)

df["sentimen"] = df["judul"].apply(
    lambda x: "Positif" if any(k in str(x).lower() for k in kamus_sentimen["positif"])
    else "Negatif" if any(k in str(x).lower() for k in kamus_sentimen["negatif"])
    else "Netral"
)

#drop judul bukan kriminal
df = df[df["judul"].apply(lambda x: not any(k in str(x) for k in kata_drop))]
df = df[df["sumber"].apply(lambda x: not any(s in str(x) for s in sumber_drop))]


# drop judul tanpa kota
df = df[(df["kota"] != "lainnya")].reset_index(drop=True)

df = df[df["tahun"] != 2026].reset_index(drop=True)

df.to_excel("fix_data.xlsx", index=False)