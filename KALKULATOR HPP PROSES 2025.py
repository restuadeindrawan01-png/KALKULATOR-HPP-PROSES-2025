import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: THEME BIRU TUA & CARD DASHBOARD ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, p, label, .stMarkdown { color: #E0E1DD !important; }
    
    /* Card Dashboard sesuai Screenshot_2025-12-27-12-05-55-89.jpg */
    .info-card { padding: 20px; border-radius: 10px; margin-bottom: 15px; color: #0D1B2A !important; }
    .card-blue { background-color: #A2D2FF; }
    .card-green { background-color: #B2D8B2; }
    .card-yellow { background-color: #E9EDC9; }

    /* Kotak Input & Tombol */
    .stNumberInput input { background-color: #FFFFFF !important; color: #0D1B2A !important; font-weight: bold; }
    .stButton>button { background-color: #1B263B; color: white; border-radius: 8px; width: 100%; border: 1px solid #778DA9; }
    
    /* Container Hasil Perhitungan */
    .result-box { background-color: #1B263B; padding: 20px; border-radius: 10px; border: 1px solid #415A77; }
    </style>
    """, unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- HEADER & NAVIGASI POJOK KANAN ATAS ---
col_jdl, col_nav = st.columns([2, 1])
with col_jdl:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")

with col_nav:
    menu = st.selectbox("Navigasi:", ["🏠 Dashboard Utama", "🏭 Kalkulator HPP"], label_visibility="collapsed")
    st.markdown('<p style="text-align:right; color:#778DA9; font-size:12px;">Pilih Menu</p>', unsafe_allow_html=True)

st.divider()

# --- HALAMAN 1: DASHBOARD ---
if menu == "🏠 Dashboard Utama":
    st.markdown("### Dashboard Kinerja Produksi")
    st.markdown("""
    <div class="info-card card-blue"><h3>Akurasi Data</h3><p>Memastikan perhitungan HPP sesuai standar PSAK.</p></div>
    <div class="info-card card-green"><h3>Efisiensi Biaya</h3><p>Memantau alokasi biaya pada Produk Dalam Proses (PDP).</p></div>
    <div class="info-card card-yellow"><h3>Laporan Otomatis</h3><p>Unit ekuivalen dan biaya per unit dihitung secara instan.</p></div>
    """, unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/accounting-concept-illustration_114360-1532.jpg", use_container_width=True)

# --- HALAMAN 2: KALKULATOR HPP ---
elif menu == "🏭 Kalkulator HPP":
    st.markdown("## 🏭 Kalkulator HPP Metode Proses")
    
    # Input Section
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 1. Data Unit Produksi")
        jadi = st.number_input("Unit Produk Jadi", min_value=0, step=1)
        pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1)
    with c2:
        st.markdown("### 2. Biaya Produksi")
        c_bbb = st.number_input("Total Biaya Bahan Baku (BBB)", min_value=0, step=1000)
        c_bk = st.number_input("Total Biaya Konversi (BTK + BOP)", min_value=0, step=1000)

    st.markdown("### 3. Tingkat Penyelesaian (%)")
    t1, t2 = st.columns(2)
    tp_bbb = t1.number_input("TP Bahan Baku (%)", 0, 100, 100) / 100
    tp_bk = t2.number_input("TP Biaya Konversi (%)", 0, 100, 50) / 100

    if st.button("🚀 HITUNG DAN TAMPILKAN LAPORAN"):
        # Perhitungan Unit Ekuivalen (UE)
        ue_bbb = jadi + (pdp * tp_bbb)
        ue_bk = jadi + (pdp * tp_bk)
        
        # Perhitungan Biaya Per Unit
        u_bbb = c_bbb / ue_bbb if ue_bbb > 0 else 0
        u_bk = c_bk / ue_bk if ue_bk > 0 else 0
        total_u = u_bbb + u_bk
        
        # Alokasi Biaya
        hpp_jadi = jadi * total_u
        hpp_pdp = (pdp * tp_bbb * u_bbb) + (pdp * tp_bk * u_bk)

        # --- TAMPILAN LAPORAN HASIL ---
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader("📋 Rincian Laporan Perhitungan")
        
        # Rincian UE & Biaya Per Unit
        res1, res2, res3 = st.columns(3)
        res1.metric("UE Bahan Baku", f"{ue_bbb} Unit")
        res2.metric("UE Biaya Konversi", f"{ue_bk} Unit")
        res3.metric("Total Biaya/Unit", format_rp(total_u))
        
        st.markdown("---")
        
        # Rincian Hasil Akhir
        st.success(f




