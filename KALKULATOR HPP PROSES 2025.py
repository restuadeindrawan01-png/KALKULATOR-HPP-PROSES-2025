import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: THEME BIRU TUA & VISUALISASI MODERN ---
st.markdown("""
    <style>
    /* Latar Belakang Biru Tua */
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, p, label, .stMarkdown { color: #E0E1DD !important; }
    
    /* Styling Kartu Dashboard (Akurasi, Efisiensi, Laporan) */
    .st-emotion-cache-p5mtre { 
        background-color: #1B263B !important; 
        border: 1px solid #415A77 !important; 
        border-radius: 12px; 
    }
    .card-content { padding: 15px; border-radius: 8px; color: #0D1B2A !important; font-weight: bold; }
    .bg-blue { background-color: #A2D2FF; }
    .bg-green { background-color: #B2D8B2; }
    .bg-yellow { background-color: #E9EDC9; }

    /* Desain Vertikal Unit Ekuivalen */
    .ue-box {
        background: linear-gradient(135deg, #1B263B 0%, #0D1B2A 100%);
        padding: 15px;
        border-left: 5px solid #778DA9;
        margin-bottom: 12px;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    .ue-label { font-size: 13px; color: #778DA9; text-transform: uppercase; letter-spacing: 1px; }
    .ue-value { font-size: 22px; font-weight: bold; color: #FFFFFF; }

    /* Input & Tombol */
    .stNumberInput input { background-color: #FFFFFF !important; color: #0D1B2A !important; font-weight: bold; }
    .stButton>button { 
        background-color: #415A77; color: white; border-radius: 8px; width: 100%; 
        border: 1px solid #778DA9; font-weight: bold; height: 50px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #778DA9; border-color: #E0E1DD; }
    </style>
    """, unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- HEADER & NAVIGASI POJOK KANAN ATAS ---
col_jdl, col_nav = st.columns([2, 1])
with col_jdl:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")
with col_nav:
    menu = st.selectbox("Menu:", ["🏠 Dashboard", "🏭 Perhitungan HPP"], label_visibility="collapsed")
    st.markdown('<p style="text-align:right; color:#778DA9; font-size:12px;">Navigasi Halaman</p>', unsafe_allow_html=True)

st.divider()

# --- HALAMAN 1: DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("## 👋 Selamat Datang di Aplikasi Kalkulator HPP")
    st.write("Klik untuk melihat penjelasan fitur utama:")
    
    with st.expander("🔵 Akurasi Data"):
        st.markdown("<div class='card-content bg-blue'>Menjamin perhitungan HPP sesuai standar PSAK dengan metode rata-rata tertimbang.</div>", unsafe_allow_html=True)
    with st.expander("🟢 Efisiensi Biaya"):
        st.markdown("<div class='card-content bg-green'>Memantau alokasi biaya pada Produk Dalam Proses (PDP) secara mendetail.</div>", unsafe_allow_html=True)
    with st.expander("🟡 Laporan Otomatis"):
        st.markdown("<div class='card-content bg-yellow'>Unit ekuivalen dan alokasi biaya akhir dihitung secara instan.</div>", unsafe_allow_html=True)
    
    st.image("https://img.freepik.com/free-vector/accounting-concept-illustration_114360-1532.jpg", use_container_width=True)

# --- HALAMAN 2: PERHITUNGAN HPP ---
elif menu == "🏭 Perhitungan HPP":
    st.markdown("### 📝 Input Data Produksi & Biaya")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.markdown("#### 1. Data Unit")
        jadi = st.number_input("Unit Produk Jadi", min_value=0, step=1)
        pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1)
        
        st.markdown("#### 2. Total Biaya Produksi")
        c_bbb = st.number_input("Biaya Bahan Baku (BBB)", min_value=0, step=1000)
        c_bbp = st.number_input("Biaya Bahan Penolong (BBP)", min_value=0, step=1000)
        c_btk = st.number_input("Biaya Tenaga Kerja (BTKL)", min_value=0, step=1000)
        c_bop = st.number_input("Biaya Overhead (BOP)", min_value=0, step=1000)

    with col_input2:
        st.markdown("#### 3. Tingkat Penyelesaian (%)")
        tp_bbb = st.number_input("TP - Bahan Baku (%)", 0, 100, 100) / 100
        tp_bbp = st.number_input("TP - Bahan Penolong (%)", 0, 100, 100) / 100
        tp_btk = st.number_input("TP - Tenaga Kerja (%)", 0, 100, 50) / 100
        tp_bop = st.number_input("TP - Overhead (%)", 0, 100, 50) / 100
        st.info("💡 Masukkan persentase penyelesaian untuk PDP Akhir di atas.")

    if st.button("🚀 JALANKAN ANALISIS BIAYA LENGKAP"):
        # Hitung Unit Ekuivalen (UE)
        ue_bbb, ue_bbp = jadi + (pdp * tp_bbb), jadi + (pdp * tp_bbp)
        ue_btk, ue_bop = jadi + (pdp * tp_btk), jadi + (pdp * tp_bop)
        
        # Biaya Per Unit
        u_bbb = c_bbb / ue_bbb if ue_bbb > 0 else 0
        u_bbp = c_bbp / ue_bbp if ue_bbp > 0 else 0
        u_btk = c_btk / ue_btk if ue_btk > 0 else 0
        u_bop = c_bop / ue_bop if ue_bop > 0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        
        # Alokasi Biaya Terpisah
        tot_hpp_jadi = jadi * total_u
        tot_hpp_pdp = (pdp*tp_bbb*u_bbb) + (pdp*tp_bbp*u_bbp) + (pdp*tp_btk*u_btk) + (pdp*tp_bop*u_bop)

        st.divider()
        
        # TAMPILAN LAPORAN HASIL
        st.markdown("### 📋 Laporan Hasil Analisis Biaya")
        
        col_res1, col_res2 = st.columns([1.5, 1])
        
        with col_res1:
            st.success(f"*Total HPP Produk Jadi*\n## {format_rp(tot_hpp_jadi)}")
            st.warning(f"*Total HPP PDP Akhir*\n## {format_rp(tot_hpp_pdp)}")
            st.info(f"*Total Biaya Keseluruhan:* {format_rp(tot_hpp_jadi + tot_hpp_pdp)}")
            st.metric("Total Biaya Per Unit", format_rp(total_u))

        with col_res2:
            st.markdown("#### 📏 Unit Ekuivalen (Rincian)")
            # Desain Vertikal
            for lab, val in [("Bahan Baku", ue_bbb), ("Bahan Penolong", ue_bbp), ("Tenaga Kerja", ue_btk), ("Overhead", ue_bop)]:
                st.markdown(f"""
                <div class="ue-box">
                    <div class="ue-label">UE {lab}</div>
                    <div class="ue-value">{val:,.1f} Unit</div>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("📚 Lihat Rumus Akuntansi"):
            st.latex(r"UE = \text{Jadi} + (\text{PDP} \times \text{TP}\%)")
            st.latex(r"\text{Biaya/Unit} = \frac{\text{Total Biaya}}{\text{UE}}")









