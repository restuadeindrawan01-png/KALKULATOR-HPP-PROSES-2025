import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS CUSTOM: THEME PROFESIONAL ---
st.markdown("""
    <style>
    /* Global Background & Font */
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, h4, p, label { color: #E0E1DD !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Input Container Glassmorphism */
    .input-section {
        background: rgba(27, 38, 59, 0.7);
        border: 1px solid rgba(119, 141, 169, 0.3);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
        margin-bottom: 20px;
    }

    /* Styling Kartu Hasil (Output) */
    .result-card {
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: none;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }
    .result-card:hover { transform: translateY(-5px); }
    .grad-blue { background: linear-gradient(135deg, #1D3557 0%, #457B9D 100%); }
    .grad-green { background: linear-gradient(135deg, #344E41 0%, #588157 100%); }

    /* Unit Ekuivalen Modern Style */
    .ue-card-modern {
        background: #1B263B;
        border-left: 5px solid #778DA9;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 10px;
    }
    .ue-card-modern small { color: #778DA9; text-transform: uppercase; letter-spacing: 1px; }

    /* Custom Button */
    .stButton>button { 
        background-color: #778DA9; color: white; border-radius: 15px; width: 100%; 
        font-weight: bold; height: 60px; font-size: 20px; border: none;
        box-shadow: 0 4px 15px rgba(119, 141, 169, 0.4);
        transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #E0E1DD; color: #0D1B2A; transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- HEADER & NAVIGASI ---
col_head, col_nav = st.columns([2, 1])
with col_head:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")
with col_nav:
    menu = st.selectbox("Pilih Menu:", ["🏠 Dashboard", "🏭 Perhitungan HPP"], label_visibility="collapsed")
    st.markdown('<p style="text-align:right; color:#778DA9; font-size:12px;">Navigasi Cepat</p>', unsafe_allow_html=True)

st.divider()

# --- DASHBOARD (SAMA SEPERTI SEBELUMNYA) ---
if menu == "🏠 Dashboard":
    st.markdown("## 👋 Selamat Datang")
    st.write("Pantau kinerja produksi dan efisiensi biaya dalam satu layar.")
    with st.expander("🔵 Akurasi Data"):
        st.info("Algoritma perhitungan HPP berbasis standar akuntansi PSAK.")
    with st.expander("🟢 Efisiensi Biaya"):
        st.success("Analisis penyerapan biaya per elemen produksi.")
    with st.expander("🟡 Laporan Otomatis"):
        st.warning("Laporan alokasi biaya instan untuk Produk Jadi dan PDP Akhir.")
    st.image("https://img.freepik.com/free-vector/data-report-concept-illustration_114360-883.jpg", use_container_width=True)

# --- MENU PERHITUNGAN HPP (DESIGN PROFESIONAL) ---
elif menu == "🏭 Perhitungan HPP":
    st.markdown("### ⚙️ Konfigurasi Biaya & Produksi")
    
    # Grid Layout 3 Kolom yang Seimbang
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("#### 📦 Volume Produksi")
        jadi = st.number_input("Unit Produk Jadi", min_value=0, step=1, key="v1")
        pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1, key="v2")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("#### 💰 Input Biaya (Total)")
        bbb = st.number_input("Bahan Baku", min_value=0, key="c1")
        bbp = st.number_input("Bahan Penolong", min_value=0, key="c2")
        btk = st.number_input("Tenaga Kerja", min_value=0, key="c3")
        bop = st.number_input("Overhead", min_value=0, key="c4")
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("#### 📈 Penyelesaian (%)")
        tp_bbb = st.number_input("TP-BBB", 0, 100, 100) / 100
        tp_bbp = st.number_input("TP-BBP", 0, 100, 100) / 100
        tp_btk = st.number_input("TP-BTK", 0, 100, 50) / 100
        tp_bop = st.number_input("TP-BOP", 0, 100, 50) / 100
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 ANALISIS HARGA POKOK PRODUKSI"):
        # Logika Inti
        ue_bbb, ue_bbp = jadi + (pdp * tp_bbb), jadi + (pdp * tp_bbp)
        ue_btk, ue_bop = jadi + (pdp * tp_btk), jadi + (pdp * tp_bop)
        
        u_bbb = bbb/ue_bbb if ue_bbb > 0 else 0
        u_bbp = bbp/ue_bbp if ue_bbp > 0 else 0
        u_btk = btk/ue_btk if ue_btk > 0 else 0
        u_bop = bop/ue_bop if ue_bop > 0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        
        h_jadi = jadi * total_u
        h_pdp = (pdp*tp_bbb*u_bbb) + (pdp*tp_bbp*u_bbp) + (pdp*tp_btk*u_btk) + (pdp*tp_bop*u_bop)

        st.markdown("---")
        st.markdown("### 📋 Laporan Hasil Analisis Produksi")
        
        res_left, res_right = st.columns([1.8, 1])
        
        with res_left:
            # Kartu Hasil dengan Gradasi
            st.markdown(f"""
                <div class="result-card grad-blue">
                    <p style="margin:0; font-weight:lighter; opacity:0.8;">HPP PRODUK JADI SELESAI</p>
                    <h1 style="margin:0; font-size:45px;">{format_rp(h_jadi)}</h1>
                </div>
                <div class="result-card grad-green">
                    <p style="margin:0; font-weight:lighter; opacity:0.8;">HPP PRODUK DALAM PROSES (PDP)</p>
                    <h1 style="margin:0; font-size:45px;">{format_rp(h_pdp)}</h1>
                </div>
            """, unsafe_allow_html=True)
            
            # Metric Panel
            m1, m2 = st.columns(2)
            m1.metric("Biaya Produksi / Unit", format_rp(total_u))
            m2.metric("Total Biaya Dialokasikan", format_rp(h_jadi + h_pdp))

        with res_right:
            st.markdown("#### 📐 Rincian Unit Ekuivalen")
            for label, value in [("Bahan Baku", ue_bbb), ("Bahan Penolong", ue_bbp), ("Tenaga Kerja", ue_btk), ("Overhead", ue_bop)]:
                st.markdown(f"""
                    <div class="ue-card-modern">
                        <small>UE {label}</small><br>
                        <span style="font-size:22px; font-weight:bold; color:#A2D2FF;">{value:,.1f} Unit</span>
                    </div>
                """, unsafe_allow_html=True)













