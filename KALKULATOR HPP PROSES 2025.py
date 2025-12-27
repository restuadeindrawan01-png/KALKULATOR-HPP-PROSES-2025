import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: BACKGROUND BIRU MUDA & NAVIGASI KANAN ---
st.markdown("""
    <style>
    /* Mengubah warna background utama menjadi biru muda */
    .stApp {
        background-color: #e3f2fd;
    }
    
    /* Menghilangkan sidebar bawaan agar bersih */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Styling kartu input */
    .stNumberInput, .stTextInput {
        background-color: white;
        border-radius: 10px;
        padding: 5px;
    }

    /* Mengubah warna tombol */
    .stButton>button {
        background-color: #1565c0;
        color: white;
        border-radius: 25px;
        font-weight: bold;
        border: none;
        height: 3em;
        width: 100%;
    }
    
    /* Menyelaraskan teks menu */
    .menu-label {
        text-align: right;
        font-weight: bold;
        color: #1565c0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI FORMAT RUPIAH TANPA DESIMAL ---
def format_rp_bulat(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- NAVIGASI POJOK KANAN ATAS ---
# Menggunakan kolom untuk mendorong menu ke kanan
col_title, col_menu = st.columns([3, 1])

with col_title:
    st.write(f"### 📊 SISTEM AKUNTANSI BIAYA")

with col_menu:
    menu = st.selectbox(
        "Pilih Halaman:",
        ["🏠 Dashboard", "🏭 Kalkulator HPP"],
        label_visibility="collapsed"
    )
    st.markdown('<p class="menu-label">Navigasi Halaman</p>', unsafe_allow_html=True)

st.markdown("---")

# --- HALAMAN 1: DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🚀 Selamat Datang!")
    st.info("Aplikasi ini membantu Anda menghitung Harga Pokok Produksi dengan metode Proses secara akurat.")
    
    dash_col1, dash_col2 = st.columns(2)
    with dash_col1:
        st.markdown("""
        *Fitur Utama:*
        * Perhitungan Unit Ekuivalen Otomatis.
        * Alokasi Biaya Produk Jadi vs PDP.
        * Input Persentase (%) secara Manual.
        * Tampilan Laporan Ringkas.
        """)
    
    with dash_col2:
        st.image("https://img.freepik.com/free-vector/data-extraction-concept-illustration_114360-4766.jpg", width=400)

# --- HALAMAN 2: KALKULATOR HPP ---
elif menu == "🏭 Kalkulator HPP":
    st.title("🏭 PERHITUNGAN HPP PROSES")
    
    # Section 1 & 2
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("1. Data Unit Produksi")
        produk_jadi = st.number_input("Unit Produk Selesai", min_value=0, step=1)
        produk_pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1)
        
    with col_input2:
        st.subheader("2. Total Biaya Produksi")
        cost_bbb = st.number_input("Total Biaya Bahan Baku (BBB)", min_value=0, step=1000)
        cost_bbp = st.number_input("Total Biaya Penolong (BBP)", min_value=0, step=1000)
        cost_btk = st.number_input("Total Biaya Tenaga Kerja (BTK)", min_value=0, step=1000)
        cost_bop = st.number_input("Total Biaya BOP", min_value=0, step=1000)

    # Section 3
    st.subheader("3. Tingkat Penyelesaian PDP (%)")
    st.caption("Masukkan angka 0 - 100")
    t1, t2, t3, t4 = st.columns(4)
    tp_bbb = t1.number_input("BBB %", 0, 100, 100) / 100
    tp_bbp = t2.number_input("BBP %", 0, 100, 100) / 100
    tp_btk = t3.number_input("BTK %", 0, 100, 50) / 100
    tp_bop = t4.number_input("BOP %", 0, 100, 50) / 100

    if st.button("✨ JALANKAN PERHITUNGAN"):
        # Logika Perhitungan UE
        ue_bbb = produk_jadi + (produk_pdp * tp_bbb)
        ue_bbp = produk_jadi + (produk_pdp * tp_bbp)
        ue_btk = produk_jadi + (produk_pdp * tp_btk)
        ue_bop = produk_jadi + (produk_pdp * tp_bop)
        
        # Biaya per Unit
        u_bbb = cost_bbb / ue_bbb if ue_bbb > 0 else 0
        u_bbp = cost_bbp / ue_bbp if ue_bbp > 0 else 0
        u_btk = cost_btk / ue_btk if ue_btk > 0 else 0
        u_bop = cost_bop / ue_bop if ue_bop > 0 else 0
        total_unit_cost = u_bbb + u_bbp + u_btk + u_bop
        
        # Alokasi
        hpp_jadi = produk_jadi * total_unit_cost
        hpp_pdp = (produk_pdp * tp_bbb * u_bbb) + (produk_pdp * tp_bbp * u_bbp) + \
                  (produk_pdp * tp_btk * u_btk) + (produk_pdp * tp_bop * u_bop)

        st.markdown("---")
        st.subheader("📋 LAPORAN BIAYA PRODUKSI")
        
        res_a, res_b = st.columns(2)
        with res_a:
            st.metric("HPP Produk Jadi", format_rp_bulat(hpp_jadi))
            st.write(f"*Unit Ekuivalen:*")
            st.write(f"• BBB: {ue_bbb} | BBP: {ue_bbp}")
            st.write(f"• BTK: {ue_btk} | BOP: {ue_bop}")

        with res_b:
            st.metric("HPP PDP Akhir", format_rp_bulat(hpp_pdp))
            st.metric("Biaya Per Unit Total", format_rp_bulat(total_unit_cost))

        with st.expander("Lihat Detail Rumus"):
            st.latex(r"UE = Jadi + (PDP \times \% TP)")
            st.latex(r"Biaya/Unit = \frac{\text{Total Biaya Unsur}}{\text{UE Unsur}}")
