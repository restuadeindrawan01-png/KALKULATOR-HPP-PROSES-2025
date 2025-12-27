import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: THEME MODERN & SPACING ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, h4, p, label, .stMarkdown { color: #E0E1DD !important; }
    
    /* Card Container untuk Input agar lebih rapi */
    .input-card {
        background-color: #1B263B;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #415A77;
        margin-bottom: 20px;
    }

    /* Styling Hasil Perhitungan */
    .result-box {
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .grad-blue { background: linear-gradient(135deg, #1d3557 0%, #457b9d 100%); border-left: 10px solid #A2D2FF; }
    .grad-green { background: linear-gradient(135deg, #344e41 0%, #588157 100%); border-left: 10px solid #B2D8B2; }

    /* Unit Ekuivalen Vertikal Modern */
    .ue-card {
        background-color: #1B263B;
        padding: 15px;
        border-radius: 10px;
        border-bottom: 3px solid #778DA9;
        margin-bottom: 12px;
    }

    .stButton>button { 
        background-color: #E0E1DD; color: #0D1B2A; border-radius: 12px; 
        width: 100%; font-weight: bold; height: 55px; font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- HEADER & NAVIGASI ---
col_title, col_nav = st.columns([2, 1])
with col_title:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")
with col_nav:
    menu = st.selectbox("Menu Utama:", ["🏠 Dashboard", "🏭 Hitung HPP"], label_visibility="collapsed")

st.divider()

# --- HALAMAN 1: DASHBOARD (TETAP SEPERTI SEMULA) ---
if menu == "🏠 Dashboard":
    st.markdown("## 👋 Selamat Datang")
    st.write("Sistem Informasi Akuntansi untuk efisiensi produksi.")
    with st.expander("🔵 Akurasi Data"):
        st.info("Menjamin perhitungan HPP sesuai standar PSAK (Metode Rata-Rata).")
    with st.expander("🟢 Efisiensi Biaya"):
        st.success("Memantau penyerapan biaya pada setiap lini produksi (PDP Akhir).")
    with st.expander("🟡 Laporan Otomatis"):
        st.warning("Laporan Unit Ekuivalen dan Alokasi Biaya dihasilkan secara instan.")
    st.image("https://img.freepik.com/free-vector/data-report-concept-illustration_114360-883.jpg", use_container_width=True)

# --- HALAMAN 2: HITUNG HPP (LEBIH MENARIK & PROPORSIONAL) ---
elif menu == "🏭 Hitung HPP":
    st.markdown("### 📝 Form Perhitungan & Laporan HPP")
    
    col_kiri, col_tengah, col_kanan = st.columns([1, 1, 1])
    
    with col_kiri:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown("#### 📦 Data Unit")
        jadi = st.number_input("Unit Produk Jadi", min_value=0, step=1, key="n1")
        pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1, key="n2")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_tengah:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown("#### 💰 Total Biaya Produksi")
        bbb = st.number_input("Biaya Bahan Baku", min_value=0, key="b1")
        bbp = st.number_input("Biaya Bahan Penolong", min_value=0, key="b2")
        btk = st.number_input("Biaya Tenaga Kerja", min_value=0, key="b3")
        bop = st.number_input("Biaya Overhead", min_value=0, key="b4")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_kanan:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown("#### ⚙️ Penyelesaian PDP (%)")
        tp_bbb = st.number_input("TP - Bahan Baku (%)", 0, 100, 100) / 100
        tp_bbp = st.number_input("TP - Bahan Penolong (%)", 0, 100, 100) / 100
        tp_btk = st.number_input("TP - Tenaga Kerja (%)", 0, 100, 50) / 100
        tp_bop = st.number_input("TP - Overhead (%)", 0, 100, 50) / 100
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 JALANKAN ANALISIS BIAYA LENGKAP"):
        # Perhitungan
        ue_bbb, ue_bbp = jadi + (pdp * tp_bbb), jadi + (pdp * tp_bbp)
        ue_btk, ue_bop = jadi + (pdp * tp_btk), jadi + (pdp * tp_bop)
        
        u_bbb = bbb/ue_bbb if ue_bbb>0 else 0
        u_bbp = bbp/ue_bbp if ue_bbp>0 else 0
        u_btk = btk/ue_btk if ue_btk>0 else 0
        u_bop = bop/ue_bop if ue_bop>0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        
        h_jadi = jadi * total_u
        h_pdp = (pdp*tp_bbb*u_bbb) + (pdp*tp_bbp*u_bbp) + (pdp*tp_btk*u_btk) + (pdp*tp_bop*u_bop)

        st.divider()
        st.markdown("### 📋 Laporan Alokasi Biaya Akhir")
        
        res_col1, res_col2 = st.columns([1.6, 1])
        
        with res_col1:
            st.markdown(f"""
                <div class="result-box grad-blue">
                    <p style="margin:0; font-size:14px; opacity:0.8;">HPP PRODUK JADI</p>
                    <h1 style="margin:0; color:white;">{format_rp(h_jadi)}</h1>
                </div>
                <div class="result-box grad-green">
                    <p style="margin:0; font-size:14px; opacity:0.8;">BIAYA PDP AKHIR</p>
                    <h1 style="margin:0; color:white;">{format_rp(h_pdp)}</h1>
                </div>
            """, unsafe_allow_html=True)
            st.metric("Total Biaya Per Unit", format_rp(total_u))

        with res_col2:
            st.markdown("#### 📐 Rincian Unit Ekuivalen")
            for lab, val in [("Bahan Baku", ue_bbb), ("Bahan Penolong", ue_bbp), ("Tenaga Kerja", ue_btk), ("Overhead", ue_bop)]:
                st.markdown(f"""
                    <div class="ue-card">
                        <small style="color:#778DA9">UE {lab}</small><br>
                        <span style="font-size:20px; font-weight:bold;">{val:,.1f} Unit</span>
                    </div>
                """, unsafe_allow_html=True)












