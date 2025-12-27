import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Proses", page_icon="🏭", layout="wide")

# --- STYLE CSS UNTUK TAMPILAN BERWARNA ---
st.markdown("""
    <style>
    /* Mengubah warna background utama */
    .stApp {
        background-color: #f0f2f6;
    }
    /* Mengubah warna sidebar */
    section[data-testid="stSidebar"] {
        background-color: #2e3b4e;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    /* Styling tombol */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        width: 100%;
    }
    /* Styling metrik */
    [data-testid="stMetricValue"] {
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI FORMAT RUPIAH TANPA ,00 ---
def format_rp_bulat(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.title("🏠 Menu Utama")
    st.markdown("---")
    menu = st.radio("Pilih Halaman:", ["📊 Dashboard", "🏭 Kalkulator HPP Proses"])
    st.markdown("---")
    st.info("Aplikasi Akuntansi Biaya v2.0")

# --- HALAMAN 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("📊 DASHBOARD KINERJA PRODUKSI")
    st.write("Selamat Datang di Sistem Informasi Akuntansi Biaya.")
    
    col_dash1, col_dash2, col_dash3 = st.columns(3)
    with col_dash1:
        st.info("### Akurasi Data\nMemastikan perhitungan HPP sesuai standar PSAK.")
    with col_dash2:
        st.success("### Efisiensi Biaya\nMemantau alokasi biaya pada Produk Dalam Proses (PDP).")
    with col_dash3:
        st.warning("### Laporan Otomatis\nUnit ekuivalen dihitung secara instan.")

    st.image("https://img.freepik.com/free-vector/factory-concept-illustration_114360-1419.jpg", width=500)

# --- HALAMAN 2: PROCESS COSTING (METODE PROSES) ---
elif menu == "🏭 Kalkulator HPP Proses":
    st.title("🏭 METODE HARGA POKOK PROSES")
    st.markdown("Gunakan formulir ini untuk menghitung alokasi biaya pada produksi massal.")

    with st.container():
        st.subheader("1. Data Produksi")
        c1, c2 = st.columns(2)
        produk_jadi = c1.number_input("Produk Selesai (Unit)", min_value=0, step=1)
        produk_pdp = c2.number_input("Produk Dalam Proses (Unit)", min_value=0, step=1)
        
        st.subheader("2. Input Total Biaya Produksi")
        b1, b2, b3, b4 = st.columns(4)
        cost_bbb = b1.number_input("Biaya Bahan Baku", min_value=0, step=1000)
        cost_bbp = b2.number_input("Biaya Penolong", min_value=0, step=1000)
        cost_btk = b3.number_input("Biaya Tenaga Kerja", min_value=0, step=1000)
        cost_bop = b4.number_input("Biaya BOP", min_value=0, step=1000)

        st.subheader("3. Input Tingkat Penyelesaian PDP (%)")
        st.caption("Masukkan angka persentase (0 - 100) secara manual")
        t1, t2, t3, t4 = st.columns(4)
        tp_bbb = t1.number_input("TP Bahan Baku (%)", 0, 100, 100) / 100
        tp_bbp = t2.number_input("TP Penolong (%)", 0, 100, 100) / 100
        tp_btk = t3.number_input("TP Tenaga Kerja (%)", 0, 100, 50) / 100
        tp_bop = t4.number_input("TP BOP (%)", 0, 100, 50) / 100

    if st.button("🚀 PROSES PERHITUNGAN BIAYA"):
        # Hitung Unit Ekuivalen (UE)
        ue_bbb = produk_jadi + (produk_pdp * tp_bbb)
        ue_bbp = produk_jadi + (produk_pdp * tp_bbp)
        ue_btk = produk_jadi + (produk_pdp * tp_btk)
        ue_bop = produk_jadi + (produk_pdp * tp_bop)
        
        # Hitung Biaya Per Unit
        unit_cost_bbb = cost_bbb / ue_bbb if ue_bbb > 0 else 0
        unit_cost_bbp = cost_bbp / ue_bbp if ue_bbp > 0 else 0
        unit_cost_btk = cost_btk / ue_btk if ue_btk > 0 else 0
        unit_cost_bop = cost_bop / ue_bop if ue_bop > 0 else 0
        total_unit_cost = unit_cost_bbb + unit_cost_bbp + unit_cost_btk + unit_cost_bop
        
        # Hitung Alokasi Biaya
        hpp_jadi = produk_jadi * total_unit_cost
        hpp_pdp = (produk_pdp * tp_bbb * unit_cost_bbb) + \
                  (produk_pdp * tp_bbp * unit_cost_bbp) + \
                  (produk_pdp * tp_btk * unit_cost_btk) + \
                  (produk_pdp * tp_bop * unit_cost_bop)

        st.divider()
        st.subheader("📋 Laporan Hasil Perhitungan")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            total_biaya = cost_bbb + cost_bbp + cost_btk + cost_bop
            st.info(f"*Total Biaya Produksi:* {format_rp_bulat(total_biaya)}")
            st.write(f"*Unit Ekuivalen (UE):*")
            st.write(f"- UE Bahan Baku: {ue_bbb}")
            st.write(f"- UE Penolong: {ue_bbp}")
            st.write(f"- UE Tenaga Kerja: {ue_btk}")
            st.write(f"- UE BOP: {ue_bop}")

        with col_res2:
            st.success(f"*HPP Produk Jadi:* {format_rp_bulat(hpp_jadi)}")
            st.warning(f"*HPP PDP Akhir:* {format_rp_bulat(hpp_pdp)}")
            st.metric("Total Biaya Per Unit", format_rp_bulat(total_unit_cost))

        with st.expander("Lihat Detail Rumus"):
            st.latex(r"UE = Jadi + (PDP \times \% TP)")
            st.latex(r"Biaya/Unit = \frac{Total Biaya Unsur}{UE Unsur}")