import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: DARK BLUE THEME & TOP RIGHT NAV ---
st.markdown("""
    <style>
    /* Mengubah seluruh latar belakang menjadi biru tua solid */
    .stApp {
        background-color: #0D1B2A !important;
    }
    
    /* Menghilangkan Sidebar sepenuhnya */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Mengatur teks judul dan deskripsi agar putih/terang */
    h1, h2, h3, p, label, .stMarkdown {
        color: #E0E1DD !important;
    }

    /* Styling Box Informasi agar biru keabu-abuan (seperti dashboard awal) */
    .stAlert {
        background-color: #1B263B !important;
        color: white !important;
        border: 1px solid #415A77;
    }

    /* Styling kotak input agar putih bersih dan mudah dibaca */
    .stNumberInput input, .stSelectbox div {
        background-color: #FFFFFF !important;
        color: #0D1B2A !important;
        font-weight: bold;
    }

    /* Styling tombol utama agar berwarna biru terang */
    .stButton>button {
        background-color: #415A77;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        border: 1px solid #778DA9;
    }

    /* Menghilangkan padding berlebih di header */
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI FORMAT RUPIAH TANPA DESIMAL ---
def format_rp_bulat(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- HEADER & NAVIGASI POJOK KANAN ATAS ---
col_judul, col_nav = st.columns([2, 1])

with col_judul:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")

with col_nav:
    # Menu navigasi diletakkan di pojok kanan atas sesuai permintaan
    menu = st.selectbox(
        "Navigasi Halaman:",
        ["📊 Dashboard", "🏭 Kalkulator HPP"],
        label_visibility="collapsed"
    )
    st.markdown('<p style="text-align:right; color:#778DA9; font-size:12px;">Pilih Halaman</p>', unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #415A77'>", unsafe_allow_html=True)

# --- HALAMAN 1: DASHBOARD (DESAIN AWAL) ---
if menu == "📊 Dashboard":
    st.markdown("## DASHBOARD KINERJA PRODUKSI")
    
    # Kolom Informasi seperti pada foto 2b7084.jpg
    dash_c1, dash_c2 = st.columns(2)
    with dash_c1:
        st.info("### Akurasi Data\nMemastikan perhitungan HPP sesuai standar PSAK agar laporan keuangan valid.")
    with dash_c2:
        st.success("### Efisiensi Biaya\nMemantau alokasi biaya pada Produk Dalam Proses (PDP) secara real-time.")
    
    st.image("https://img.freepik.com/free-vector/modern-data-report-concept-illustration_114360-2646.jpg", width=500)

# --- HALAMAN 2: KALKULATOR HPP ---
elif menu == "🏭 Kalkulator HPP":
    st.markdown("## 🏭 Kalkulator HPP Metode Proses")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 1. Data Unit")
        produk_jadi = st.number_input("Unit Produk Selesai", min_value=0, step=1)
        produk_pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1)
        
    with col2:
        st.markdown("### 2. Biaya Produksi")
        cost_bbb = st.number_input("Biaya Bahan Baku", min_value=0, step=1000)
        cost_bbp = st.number_input("Biaya Bahan Penolong", min_value=0, step=1000)
        cost_btk = st.number_input("Biaya Tenaga Kerja", min_value=0, step=1000)
        cost_bop = st.number_input("Biaya BOP", min_value=0, step=1000)

    st.markdown("### 3. Tingkat Penyelesaian (%)")
    t1, t2, t3, t4 = st.columns(4)
    tp_bbb = t1.number_input("BBB (%)", 0, 100, 100) / 100
    tp_bbp = t2.number_input("BBP (%)", 0, 100, 100) / 100
    tp_btk = t3.number_input("BTK (%)", 0, 100, 50) / 100
    tp_bop = t4.number_input("BOP (%)", 0, 100, 50) / 100

    if st.button("🚀 PROSES PERHITUNGAN"):
        # Logika Perhitungan
        ue_bbb = produk_jadi + (produk_pdp * tp_bbb)
        ue_bbp = produk_jadi + (produk_pdp * tp_bbp)
        ue_btk = produk_jadi + (produk_pdp * tp_btk)
        ue_bop = produk_jadi + (produk_pdp * tp_bop)
        
        u_bbb = cost_bbb / ue_bbb if ue_bbb > 0 else 0
        u_bbp = cost_bbp / ue_bbp if ue_bbp > 0 else 0
        u_btk = cost_btk / ue_btk if ue_btk > 0 else 0
        u_bop = cost_bop / ue_bop if ue_bop > 0 else 0
        total_unit = u_bbb + u_bbp + u_btk + u_bop
        
        hpp_jadi = produk_jadi * total_unit
        hpp_pdp = (produk_pdp * tp_bbb * u_bbb) + (produk_pdp * tp_bbp * u_bbp) + \
                  (produk_pdp * tp_btk * u_btk) + (produk_pdp * tp_bop * u_bop)

        st.markdown("<hr style='border:1px solid #778DA9'>", unsafe_allow_html=True)
        st.subheader("📋 HASIL LAPORAN BIAYA")
        
        res1, res2 = st.columns(2)
        with res1:
            st.metric("HPP Produk Jadi", format_rp_bulat(hpp_jadi))
            st.write(f"*Unit Ekuivalen:*\nBBB: {ue_bbb} | BBP: {ue_bbp}")
        with res2:
            st.metric("HPP PDP Akhir", format_rp_bulat(hpp_pdp))
            st.metric("Total Biaya Per Unit", format_rp_bulat(total_unit))


