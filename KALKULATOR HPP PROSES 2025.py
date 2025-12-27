import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: BACKGROUND BIRU & NAVIGASI KANAN ---
st.markdown("""
    <style>
    /* Mengubah warna background utama menjadi biru muda */
    .stApp {
        background-color: #e3f2fd;
    }
    
    /* Menghilangkan sidebar agar tampilan bersih */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Styling input agar tetap kontras (putih) */
    .stNumberInput, .stTextInput {
        background-color: white;
        border-radius: 10px;
    }

    /* Mengubah warna tombol utama */
    .stButton>button {
        background-color: #1565c0;
        color: white;
        border-radius: 25px;
        font-weight: bold;
        width: 100%;
        border: none;
    }
    
    /* Label navigasi di kanan */
    .menu-label {
        text-align: right;
        font-size: 0.8rem;
        color: #1565c0;
        margin-top: -15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI FORMAT RUPIAH BULAT ---
def format_rp_bulat(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- BARIS NAVIGASI ATAS ---
# Membagi layar: Judul di kiri (3/4), Menu di kanan (1/4)
col_judul, col_nav = st.columns([3, 1])

with col_judul:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")

with col_nav:
    # Menu dropdown di pojok kanan atas
    menu = st.selectbox(
        "Pilih Halaman:",
        ["🏠 Dashboard", "🏭 Kalkulator HPP"],
        label_visibility="collapsed"
    )
    st.markdown('<p class="menu-label">Navigasi Menu</p>', unsafe_allow_html=True)

st.markdown("---")

# --- LOGIKA HALAMAN ---
if menu == "🏠 Dashboard":
    st.subheader("Selamat Datang!")
    st.info("Gunakan menu di pojok kanan atas untuk mulai menghitung HPP.")
    st.image("https://img.freepik.com/free-vector/data-extraction-concept-illustration_114360-4766.jpg", width=400)

elif menu == "🏭 Kalkulator HPP":
    st.subheader("🏭 Perhitungan HPP Metode Proses")
    
    # Input Data
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 1. Data Unit")
        produk_jadi = st.number_input("Unit Produk Selesai", min_value=0, step=1)
        produk_pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1)
        
    with c2:
        st.markdown("### 2. Biaya Produksi")
        cost_bbb = st.number_input("Total Biaya Bahan Baku", min_value=0, step=1000)
        cost_bbp = st.number_input("Total Biaya Penolong", min_value=0, step=1000)
        cost_btk = st.number_input("Total Tenaga Kerja", min_value=0, step=1000)
        cost_bop = st.number_input("Total Biaya BOP", min_value=0, step=1000)

    st.markdown("### 3. Tingkat Penyelesaian PDP (%)")
    t1, t2, t3, t4 = st.columns(4)
    tp_bbb = t1.number_input("BBB (%)", 0, 100, 100) / 100
    tp_bbp = t2.number_input("BBP (%)", 0, 100, 100) / 100
    tp_btk = t3.number_input("BTK (%)", 0, 100, 50) / 100
    tp_bop = t4.number_input("BOP (%)", 0, 100, 50) / 100

    if st.button("✨ HITUNG HPP"):
        # Hitung Unit Ekuivalen
        ue_bbb = produk_jadi + (produk_pdp * tp_bbb)
        ue_bbp = produk_jadi + (produk_pdp * tp_bbp)
        ue_btk = produk_jadi + (produk_pdp * tp_btk)
        ue_bop = produk_jadi + (produk_pdp * tp_bop)
        
        # Biaya per Unit
        u_bbb = cost_bbb / ue_bbb if ue_bbb > 0 else 0
        u_bbp = cost_bbp / ue_bbp if ue_bbp > 0 else 0
        u_btk = cost_btk / ue_btk if ue_btk > 0 else 0
        u_bop = cost_bop / ue_bop if ue_bop > 0 else 0
        total_unit = u_bbb + u_bbp + u_btk + u_bop
        
        # Alokasi
        hpp_jadi = produk_jadi * total_unit
        hpp_pdp = (produk_pdp * tp_bbb * u_bbb) + (produk_pdp * tp_bbp * u_bbp) + \
                  (produk_pdp * tp_btk * u_btk) + (produk_pdp * tp_bop * u_bop)

        st.markdown("---")
        st.success(f"*HPP Produk Jadi:* {format_rp_bulat(hpp_jadi)}")
        st.warning(f"*HPP PDP Akhir:* {format_rp_bulat(hpp_pdp)}")
        st.metric("Total Biaya Per Unit", format_rp_bulat(total_unit))

