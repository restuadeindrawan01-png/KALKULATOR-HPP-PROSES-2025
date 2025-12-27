import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: THEME BIRU TUA & KOTAK DASHBOARD ---
st.markdown("""
    <style>
    /* Mengubah latar belakang menjadi biru tua */
    .stApp {
        background-color: #0D1B2A !important;
    }
    
    /* Menghilangkan Sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Warna teks umum menjadi putih terang */
    h1, h2, h3, p, label, .stMarkdown {
        color: #E0E1DD !important;
    }

    /* Styling Kotak Dashboard (Card) sesuai gambar awal */
    .info-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #0D1B2A !important; /* Teks dalam kotak tetap gelap agar terbaca */
    }
    .card-blue { background-color: #A2D2FF; }
    .card-green { background-color: #B2D8B2; }
    .card-yellow { background-color: #E9EDC9; }

    /* Styling Input & Selectbox */
    .stNumberInput input, .stSelectbox div {
        background-color: #FFFFFF !important;
        color: #0D1B2A !important;
    }

    /* Tombol Perhitungan */
    .stButton>button {
        background-color: #1B263B;
        color: white;
        border-radius: 8px;
        width: 100%;
        border: 1px solid #778DA9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI FORMAT RUPIAH ---
def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- NAVIGASI POJOK KANAN ATAS ---
col_jdl, col_nav = st.columns([2, 1])
with col_jdl:
    st.markdown("# 📊 DASHBOARD KINERJA PRODUKSI")

with col_nav:
    menu = st.selectbox(
        "Pilih Menu:",
        ["🏠 Dashboard Utama", "🏭 Kalkulator HPP"],
        label_visibility="collapsed"
    )
    st.markdown('<p style="text-align:right; color:#778DA9; font-size:12px;">Navigasi Halaman</p>', unsafe_allow_html=True)

st.divider()

# --- HALAMAN 1: DASHBOARD (SESUAI GAMBAR) ---
if menu == "🏠 Dashboard Utama":
    st.write("Selamat Datang di Sistem Informasi Akuntansi Biaya.")
    
    # Grid Kotak Informasi sesuai gambar Screenshot_2025-12-27-12-05-55-89.jpg
    st.markdown("""
    <div class="info-card card-blue">
        <h3>Akurasi Data</h3>
        <p>Memastikan perhitungan HPP sesuai standar PSAK.</p>
    </div>
    <div class="info-card card-green">
        <h3>Efisiensi Biaya</h3>
        <p>Memantau alokasi biaya pada Produk Dalam Proses (PDP).</p>
    </div>
    <div class="info-card card-yellow">
        <h3>Laporan Otomatis</h3>
        <p>Unit ekuivalen dihitung secara instan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gambar ilustrasi di bawah dasbor
    st.markdown("### Ilustrasi Alur Perhitungan")
    st.image("https://img.freepik.com/free-vector/accounting-concept-illustration_114360-1532.jpg", 
             caption="Proses Akuntansi Biaya Produksi", use_container_width=True)

# --- HALAMAN 2: KALKULATOR HPP ---
elif menu == "🏭 Kalkulator HPP":
    st.subheader("🏭 Form Perhitungan HPP Proses")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 1. Data Unit")
        produk_jadi = st.number_input("Unit Selesai", min_value=0, step=1)
        produk_pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1)
        
    with c2:
        st.markdown("### 2. Biaya Produksi")
        cost_bbb = st.number_input("Biaya Bahan Baku", min_value=0, step=1000)
        cost_bbp = st.number_input("Biaya Bahan Penolong", min_value=0, step=1000)
        cost_btk = st.number_input("Biaya Tenaga Kerja", min_value=0, step=1000)
        cost_bop = st.number_input("Biaya BOP", min_value=0, step=1000)

    st.markdown("### 3. Tingkat Penyelesaian (%)")
    t1, t2, t3, t4 = st.columns(4)
    tp_bbb = t1.number_input("BBB %", 0, 100, 100) / 100
    tp_bbp = t2.number_input("BBP %", 0, 100, 100) / 100
    tp_btk = t3.number_input("BTK %", 0, 100, 50) / 100
    tp_bop = t4.number_input("BOP %", 0, 100, 50) / 100

    if st.button("🚀 HITUNG SEKARANG"):
        ue_bbb = produk_jadi + (produk_pdp * tp_bbb)
        ue_bbp = produk_jadi + (produk_pdp * tp_bbp)
        ue_btk = produk_jadi + (produk_pdp * tp_btk)
        ue_bop = produk_jadi + (produk_pdp * tp_bop)
        
        u_bbb = cost_bbb / ue_bbb if ue_bbb > 0 else 0
        u_bbp = cost_bbp / ue_bbp if ue_bbp > 0 else 0
        u_btk = cost_btk / ue_btk if ue_btk > 0 else 0
        u_bop = cost_bop / ue_bop if ue_bop > 0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        
        st.divider()
        st.success(f"*HPP Produk Jadi:* {format_rp(produk_jadi * total_u)}")
        st.metric("Total Biaya Per Unit", format_rp(total_u))



