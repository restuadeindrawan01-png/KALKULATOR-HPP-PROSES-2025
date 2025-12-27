import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: PREMIUM DARK MODE ---
st.markdown("""
    <style>
    /* Latar Belakang & Font Global */
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, h4, p, label, .stMarkdown { color: #E0E1DD !important; font-family: 'Inter', sans-serif; }
    
    /* Kartu Hasil Perhitungan (Output) */
    .card-output {
        padding: 35px;
        border-radius: 20px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .blue-grad { background: linear-gradient(135deg, #1d3557 0%, #457b9d 100%); }
    .green-grad { background: linear-gradient(135deg, #344e41 0%, #588157 100%); }

    /* Unit Ekuivalen Modern Vertikal */
    .ue-modern {
        background: #1B263B;
        padding: 15px 20px;
        margin-bottom: 12px;
        border-radius: 12px;
        border-left: 6px solid #778DA9;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .ue-val { font-size: 22px; font-weight: 800; color: #A2D2FF; }

    /* Tombol Analisis Besar */
    .stButton>button { 
        background: linear-gradient(90deg, #415A77 0%, #778DA9 100%);
        color: white; border-radius: 15px; width: 100%; font-weight: bold; 
        height: 65px; font-size: 22px; border: none; margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stButton>button:hover { background: #E0E1DD; color: #0D1B2A; transform: scale(1.01); }
    </style>
""", unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- NAVIGASI HEADER ---
c_head, c_nav = st.columns([2.5, 1])
with c_head:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")
with c_nav:
    menu = st.selectbox("", ["🏠 Dashboard", "🏭 Perhitungan HPP"], label_visibility="collapsed")
    st.markdown('<p style="text-align:right; color:#778DA9; font-size:13px; margin-top:-10px;">Navigasi Panel</p>', unsafe_allow_html=True)

st.divider()

# --- HALAMAN DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("## 👋 Selamat Datang di Dashboard Utama")
    st.write("Sistem Informasi Akuntansi Biaya untuk efisiensi produksi.")
    with st.expander("🔵 Akurasi Data"):
        st.info("Perhitungan HPP sesuai standar PSAK (Metode Rata-Rata).")
    with st.expander("🟢 Efisiensi Biaya"):
        st.success("Pantau penyerapan biaya per elemen produksi secara mendetail.")
    with st.expander("🟡 Laporan Otomatis"):
        st.warning("Unit ekuivalen dan biaya dialokasikan secara instan.")
    
    # GAMBAR KOTAK BESAR DI DASHBOARD TELAH DIHAPUS UNTUK MENGHEMAT RUANG

# --- HALAMAN PERHITUNGAN HPP ---
elif menu == "🏭 Perhitungan HPP":
    st.markdown("### ⚙️ Konfigurasi Biaya & Data Produksi")
    
    c1, c2, c3 = st.columns(3, gap="large")
    
    with c1:
        st.markdown('<div class="input-box">', unsafe_allow_html=True)
        st.markdown("#### 📦 Volume Unit")
        # Ikon tetap dipertahankan namun ukuran tetap kecil (60px)
        st.image("https://cdn-icons-png.flaticon.com/512/5164/5164023.png", width=60)
        st.write("Masukkan data kuantitas barang.")
        jadi = st.number_input("Unit Selesai (Jadi)", min_value=0, step=1)
        pdp = st.number_input("Unit Belum Selesai (PDP)", min_value=0, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="input-box">', unsafe_allow_html=True)
        st.markdown("#### 💰 Alokasi Biaya")
        st.image("https://cdn-icons-png.flaticon.com/512/2454/2454282.png", width=60)
        st.write("Input total biaya yang terjadi.")
        bbb = st.number_input("Biaya Bahan Baku", min_value=0)
        bbp = st.number_input("Biaya Bahan Penolong", min_value=0)
        btk = st.number_input("Biaya Tenaga Kerja", min_value=0)
        bop = st.number_input("Biaya Overhead", min_value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="input-box">', unsafe_allow_html=True)
        st.markdown("#### 📈 Progress PDP (%)")
        st.image("https://cdn-icons-png.flaticon.com/512/1548/1548914.png", width=60)
        st.write("Tingkat penyelesaian barang.")
        tp_bbb = st.number_input("Penyelesaian BBB (%)", 0, 100, 100) / 100
        tp_bbp = st.number_input("Penyelesaian BBP (%)", 0, 100, 100) / 100
        tp_btk = st.number_input("Penyelesaian BTK (%)", 0, 100, 50) / 100
        tp_bop = st.number_input("Penyelesaian BOP (%)", 0, 100, 50) / 100
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 JALANKAN ANALISIS HPP SEKARANG"):
        # Logika Kalkulator
        ue_bbb, ue_bbp = jadi + (pdp * tp_bbb), jadi + (pdp * tp_bbp)
        ue_btk = jadi + (pdp * tp_btk)
        ue_bop = jadi + (pdp * tp_bop)
        
        u_bbb = bbb/ue_bbb if ue_bbb > 0 else 0
        u_bbp = bbp/ue_bbp if ue_bbp > 0 else 0
        u_btk = btk/ue_btk if ue_btk > 0 else 0
        u_bop = bop/ue_bop if ue_bop > 0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        h_jadi, h_pdp = jadi * total_u, (pdp*tp_bbb*u_bbb) + (pdp*tp_bbp*u_bbp) + (pdp*tp_btk*u_btk) + (pdp*tp_bop*u_bop)

        st.divider()
        st.markdown("### 📋 Laporan Hasil Alokasi Biaya")
        
        res_l, res_r = st.columns([1.8, 1], gap="medium")
        
        with res_l:
            st.markdown(f"""
                <div class="card-output blue-grad">
                    <p style="margin:0; opacity:0.8;">HPP PRODUK JADI SELESAI</p>
                    <h1 style="margin:0; font-size:50px;">{format_rp(h_jadi)}</h1>
                </div>
                <div class="card-output green-grad">
                    <p style="margin:0; opacity:0.8;">BIAYA PRODUK DALAM PROSES (PDP)</p>
                    <h1 style="margin:0; font-size:50px;">{format_rp(h_pdp)}</h1>
                </div>
            """, unsafe_allow_html=True)
            st.metric("Total Biaya Per Unit Produksi", format_rp(total_u))

        with res_r:
            st.markdown("#### 📏 Rincian Unit Ekuivalen")
            for l, v in [("BBB", ue_bbb), ("BBP", ue_bbp), ("BTK", ue_btk), ("BOP", ue_bop)]:
                st.markdown(f"""
                    <div class="ue-modern">
                        <span>UE {l}</span>
                        <span class="ue-val">{v:,.1f}</span>
                    </div>
                """, unsafe_allow_html=True)



















