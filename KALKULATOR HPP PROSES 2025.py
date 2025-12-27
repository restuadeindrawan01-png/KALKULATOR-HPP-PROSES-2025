import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: THEME BIRU TUA & VISUALISASI HASIL ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, p, label, .stMarkdown { color: #E0E1DD !important; }
    
    /* Card Dashboard & Penjelasan */
    .st-emotion-cache-p5mtre { 
        background-color: #1B263B !important; 
        border: 1px solid #415A77 !important; 
        border-radius: 12px; 
    }
    .card-content { padding: 15px; border-radius: 8px; color: #0D1B2A !important; font-weight: bold; }
    .bg-blue { background-color: #A2D2FF; }
    .bg-green { background-color: #B2D8B2; }
    .bg-yellow { background-color: #E9EDC9; }

    /* Kotak Hasil Perhitungan Vertikal */
    .ue-container {
        background-color: #1B263B;
        padding: 15px;
        border-left: 5px solid #415A77;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .metric-label { font-size: 14px; color: #778DA9; }
    .metric-value { font-size: 20px; font-weight: bold; color: #E0E1DD; }

    /* Input & Button */
    .stNumberInput input { background-color: #FFFFFF !important; color: #0D1B2A !important; }
    .stButton>button { 
        background-color: #415A77; color: white; border-radius: 8px; width: 100%; 
        border: 1px solid #778DA9; font-weight: bold; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- HEADER & NAVIGASI ---
col_jdl, col_nav = st.columns([2, 1])
with col_jdl:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")
with col_nav:
    menu = st.selectbox("Menu:", ["🏠 Dashboard", "🏭 Perhitungan HPP"], label_visibility="collapsed")
    st.markdown('<p style="text-align:right; color:#778DA9; font-size:12px;">Pilih Menu</p>', unsafe_allow_html=True)

st.divider()

# --- HALAMAN 1: DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("## 👋 Selamat Datang di Aplikasi Kalkulator HPP")
    with st.expander("🔵 Akurasi Data"):
        st.markdown("<div class='card-content bg-blue'>Menjamin perhitungan sesuai standar PSAK dengan metode rata-rata tertimbang.</div>", unsafe_allow_html=True)
    with st.expander("🟢 Efisiensi Biaya"):
        st.markdown("<div class='card-content bg-green'>Memantau penyerapan biaya pada Produk Dalam Proses (PDP) secara real-time.</div>", unsafe_allow_html=True)
    with st.expander("🟡 Laporan Otomatis"):
        st.markdown("<div class='card-content bg-yellow'>Menghasilkan rincian unit ekuivalen dan alokasi biaya secara instan.</div>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/accounting-concept-illustration_114360-1532.jpg", use_container_width=True)

# --- HALAMAN 2: PERHITUNGAN HPP ---
elif menu == "🏭 Perhitungan HPP":
    st.markdown("### 📝 Input Data Produksi")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 1. Data Unit")
        jadi = st.number_input("Unit Produk Jadi", min_value=0, step=1)
        pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1)
        
        st.markdown("#### 2. Rincian Biaya")
        c_bbb = st.number_input("Biaya Bahan Baku (BBB)", min_value=0)
        c_bbp = st.number_input("Biaya Bahan Penolong (BBP)", min_value=0)
        c_btk = st.number_input("Biaya Tenaga Kerja (BTKL)", min_value=0)
        c_bop = st.number_input("Biaya Overhead (BOP)", min_value=0)

    with col2:
        st.markdown("#### 3. Tingkat Penyelesaian (%)")
        tp_bbb = st.slider("TP - Bahan Baku", 0, 100, 100) / 100
        tp_bbp = st.slider("TP - Bahan Penolong", 0, 100, 100) / 100
        tp_btk = st.slider("TP - Tenaga Kerja", 0, 100, 50) / 100
        tp_bop = st.slider("TP - Overhead", 0, 100, 50) / 100

    if st.button("🚀 JALANKAN ANALISIS BIAYA"):
        # Perhitungan Unit Ekuivalen (UE)
        ue_bbb, ue_bbp = jadi + (pdp * tp_bbb), jadi + (pdp * tp_bbp)
        ue_btk, ue_bop = jadi + (pdp * tp_btk), jadi + (pdp * tp_bop)
        
        # Biaya Per Unit
        u_bbb = c_bbb / ue_bbb if ue_bbb > 0 else 0
        u_bbp = c_bbp / ue_bbp if ue_bbp > 0 else 0
        u_btk = c_btk / ue_btk if ue_btk > 0 else 0
        u_bop = c_bop / ue_bop if ue_bop > 0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        
        # Alokasi
        tot_hpp_jadi = jadi * total_u
        tot_hpp_pdp = (pdp*tp_bbb*u_bbb) + (pdp*tp_bbp*u_bbp) + (pdp*tp_btk*u_btk) + (pdp*tp_bop*u_bop)

        st.divider()
        
        # TAMPILAN HASIL (Pemisahan Jadi & PDP serta UE Vertikal)
        res_col1, res_col2 = st.columns([1.5, 1])
        
        with res_col1:
            st.markdown("#### 📦 Hasil Alokasi Biaya")
            st.success(f"*Total HPP Produk Jadi:* \n## {format_rp(tot_hpp_jadi)}")
            st.warning(f"*Total HPP PDP Akhir:* \n## {format_rp(tot_hpp_pdp)}")
            st.info(f"*Total Biaya Produksi:* \n{format_rp(tot_hpp_jadi + tot_hpp_pdp)}")

        with res_col2:
            st.markdown("#### 📏 Rincian Unit Ekuivalen")
            # Tampilan Vertikal yang Menarik
            ue_data = [("BBB", ue_bbb), ("BBP", ue_bbp), ("BTK", ue_btk), ("BOP", ue_bop)]
            for label, val in ue_data:
                st.markdown(f"""
                <div class="ue-container">
                    <div class="metric-label">Unit Ekuivalen {label}</div>
                    <div class="metric-value">{val} Unit</div>
                </div>
                """, unsafe_allow_html=True)
            st.metric("Total Biaya / Unit", format_rp(total_u))

        with st.expander("📚 Rumus Akuntansi yang Digunakan"):
            st.latex(r"UE = \text{Unit Jadi} + (\text{Unit PDP} \times \text{TP}\%)")
            st.latex(r"\text{HPP PDP Akhir} = \sum (\text{Unit PDP} \times \text{TP} \times \text{Biaya/Unit})")







