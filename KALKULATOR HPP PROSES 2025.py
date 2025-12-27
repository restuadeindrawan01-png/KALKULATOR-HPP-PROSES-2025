import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: THEME BIRU TUA & CARD DASHBOARD ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, p, label, .stMarkdown { color: #E0E1DD !important; }
    
    /* Styling Kartu Dashboard agar seperti Screenshot_2025-12-27-12-05-55-89.jpg */
    .st-emotion-cache-p5mtre { 
        background-color: #1B263B !important; 
        border: 1px solid #415A77 !important; 
        border-radius: 12px; 
    }
    
    .card-content { padding: 15px; border-radius: 8px; color: #0D1B2A !important; font-weight: 500; }
    .bg-blue { background-color: #A2D2FF; }
    .bg-green { background-color: #B2D8B2; }
    .bg-yellow { background-color: #E9EDC9; }

    /* Styling Input & Tombol */
    .stNumberInput input { background-color: #FFFFFF !important; color: #0D1B2A !important; font-weight: bold; }
    .stButton>button { 
        background-color: #415A77; 
        color: white; 
        border-radius: 8px; 
        width: 100%; 
        border: 1px solid #778DA9; 
        font-weight: bold;
    }
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
    st.markdown("## 👋 Selamat Datang di Aplikasi Kalkulator HPP Akuntansi")
    st.write("Silakan klik menu di bawah ini untuk melihat penjelasan lengkap fungsionalitas sistem:")

    # Menu Interaktif sesuai permintaan
    with st.expander("🔵 Akurasi Data"):
        st.markdown("""
        <div class='card-content bg-blue'>
        <strong>Penjelasan:</strong> Memastikan setiap perhitungan Harga Pokok Produksi (HPP) mengikuti standar <strong>PSAK</strong>. 
        Sistem menggunakan metode rata-rata tertimbang untuk menjamin akurasi nilai persediaan dan laporan laba rugi Anda.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🟢 Efisiensi Biaya"):
        st.markdown("""
        <div class='card-content bg-green'>
        <strong>Penjelasan:</strong> Membantu manajemen memantau alokasi biaya secara real-time pada <strong>Produk Dalam Proses (PDP)</strong>. 
        Dengan rincian biaya per unsur, Anda dapat mendeteksi pemborosan sejak dini di lini produksi.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🟡 Laporan Otomatis"):
        st.markdown("""
        <div class='card-content bg-yellow'>
        <strong>Penjelasan:</strong> Unit ekuivalen dan biaya per unit dihitung secara instan. 
        Anda tidak perlu lagi melakukan perhitungan manual yang rumit untuk membagi biaya antara produk jadi dan produk dalam proses.
        </div>
        """, unsafe_allow_html=True)

    st.image("https://img.freepik.com/free-vector/accounting-concept-illustration_114360-1532.jpg", use_container_width=True)

# --- HALAMAN 2: KALKULATOR HPP (LENGKAP) ---
elif menu == "🏭 Kalkulator HPP":
    st.markdown("## 🏭 Form Perhitungan HPP & Laporan Rinci")
    
    # 1. Data Unit
    st.markdown("### 1. Data Unit Produksi")
    cu1, cu2 = st.columns(2)
    jadi = cu1.number_input("Unit Produk Jadi", min_value=0, step=1)
    pdp = cu2.number_input("Unit PDP Akhir", min_value=0, step=1)

    # 2. Rincian Biaya Lengkap
    st.markdown("### 2. Rincian Total Biaya Produksi")
    cb1, cb2 = st.columns(2)
    c_bbb = cb1.number_input("Biaya Bahan Baku (BBB)", min_value=0, step=1000)
    c_bbp = cb2.number_input("Biaya Bahan Penolong (BBP)", min_value=0, step=1000)
    c_btk = cb1.number_input("Biaya Tenaga Kerja (BTKL)", min_value=0, step=1000)
    c_bop = cb2.number_input("Biaya Overhead Pabrik (BOP)", min_value=0, step=1000)

    # 3. Tingkat Penyelesaian
    st.markdown("### 3. Tingkat Penyelesaian PDP Akhir (%)")
    t1, t2, t3, t4 = st.columns(4)
    tp_bbb = t1.number_input("BBB %", 0, 100, 100) / 100
    tp_bbp = t2.number_input("BBP %", 0, 100, 100) / 100
    tp_btk = t3.number_input("BTK %", 0, 100, 50) / 100
    tp_bop = t4.number_input("BOP %", 0, 100, 50) / 100

    if st.button("🚀 JALANKAN PERHITUNGAN LENGKAP"):
        # Hitung UE & Biaya Per Unit
        ue_bbb, ue_bbp = jadi + (pdp*tp_bbb), jadi + (pdp*tp_bbp)
        ue_btk, ue_bop = jadi + (pdp*tp_btk), jadi + (pdp*tp_bop)
        
        u_bbb, u_bbp = c_bbb/ue_bbb if ue_bbb>0 else 0, c_bbp/ue_bbp if ue_bbp>0 else 0
        u_btk, u_bop = c_btk/ue_btk if ue_btk>0 else 0, c_bop/ue_bop if ue_bop>0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        
        # Alokasi
        hpp_jadi = jadi * total_u
        hpp_pdp = (pdp*tp_bbb*u_bbb) + (pdp*tp_bbp*u_bbp) + (pdp*tp_btk*u_btk) + (pdp*tp_bop*u_bop)

        # Laporan
        st.divider()
        st.subheader("📋 Laporan Hasil Analisis")
        res1, res2 = st.columns(2)
        with res1:
            st.metric("Total HPP Produk Jadi", format_rp(hpp_jadi))
            st.write(f"*Unit Ekuivalen:*\nBBB: {ue_bbb} | BBP: {ue_bbp}\nBTK: {ue_btk} | BOP: {ue_bop}")
        with res2:
            st.metric("Total HPP PDP Akhir", format_rp(hpp_pdp))
            st.metric("Biaya Per Unit Total", format_rp(total_u))

        with st.expander("📚 Lihat Rumus Akuntansi"):
            st.latex(r"UE = \text{Jadi} + (\text{PDP} \times \text{TP}\%)")
            st.latex(r"\text{Biaya/Unit} = \frac{\text{Total Biaya}}{\text{Unit Ekuivalen}}")






