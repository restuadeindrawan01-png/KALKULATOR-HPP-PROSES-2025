import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS UNTUK TAMPILAN MODERN & BERJARAK ---
st.markdown("""
    <style>
    /* Latar belakang gelap elegan */
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, p, label, .stMarkdown { color: #E0E1DD !important; }
    
    /* Memberi jarak antar elemen input */
    .stNumberInput { margin-bottom: 25px !important; }
    
    /* Styling Kartu Dashboard */
    .st-emotion-cache-p5mtre { 
        background-color: #1B263B !important; 
        border: 1px solid #415A77 !important; 
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    /* Box Hasil Perhitungan dengan Bayangan */
    .result-card {
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .bg-jadi { background: linear-gradient(135deg, #1d3557 0%, #457b9d 100%); }
    .bg-pdp { background: linear-gradient(135deg, #344e41 0%, #588157 100%); }

    /* Unit Ekuivalen Vertikal Berjarak */
    .ue-item {
        background-color: #1B263B;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #E0E1DD;
        margin-bottom: 15px;
    }
    
    /* Tombol Besar */
    .stButton>button { 
        background-color: #E0E1DD; color: #0D1B2A; border-radius: 10px; width: 100%; 
        font-weight: bold; height: 60px; font-size: 18px; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- NAVIGASI POJOK KANAN ---
col_jdl, col_nav = st.columns([2, 1])
with col_jdl:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")
with col_nav:
    menu = st.selectbox("Pilih Menu:", ["🏠 Dashboard", "🏭 Hitung HPP"], label_visibility="collapsed")

st.divider()

if menu == "🏠 Dashboard":
    st.markdown("## 👋 Selamat Datang")
    st.write("Sistem Informasi Akuntansi untuk efisiensi produksi.")
    
    # Dashboard Berjarak
    with st.expander("🔵 Akurasi Data"):
        st.info("Menjamin perhitungan HPP sesuai standar PSAK (Metode Rata-Rata).")
    with st.expander("🟢 Efisiensi Biaya"):
        st.success("Memantau penyerapan biaya pada setiap lini produksi (PDP Akhir).")
    with st.expander("🟡 Laporan Otomatis"):
        st.warning("Laporan Unit Ekuivalen dan Alokasi Biaya dihasilkan secara instan.")
    
    st.image("https://img.freepik.com/free-vector/data-report-concept-illustration_114360-883.jpg", use_container_width=True)

elif menu == "🏭 Hitung HPP":
    st.markdown("### 📝 Input Data Produksi")
    st.write("Isi data di bawah ini dengan teliti.")
    
    # Menggunakan Container untuk memberi jarak visual
    with st.container():
        c1, spacer, c2 = st.columns([1, 0.2, 1]) # Menambahkan 'spacer' di tengah
        
        with c1:
            st.markdown("#### 📦 Data Unit")
            jadi = st.number_input("Jumlah Unit Produk Jadi", min_value=0, step=1)
            pdp = st.number_input("Jumlah Unit PDP Akhir", min_value=0, step=1)
            
            st.markdown("---") # Garis pemisah antar bagian
            st.markdown("#### 💰 Rincian Total Biaya")
            bbb = st.number_input("Total Biaya Bahan Baku (BBB)", min_value=0)
            bbp = st.number_input("Total Biaya Bahan Penolong (BBP)", min_value=0)
            btk = st.number_input("Total Biaya Tenaga Kerja (BTKL)", min_value=0)
            bop = st.number_input("Total Biaya Overhead (BOP)", min_value=0)

        with c2:
            st.markdown("#### ⚙️ Tingkat Penyelesaian (%)")
            st.write("Masukkan persentase penyelesaian untuk PDP Akhir:")
            tp_bbb = st.number_input("TP - Bahan Baku (%)", 0, 100, 100) / 100
            tp_bbp = st.number_input("TP - Bahan Penolong (%)", 0, 100, 100) / 100
            tp_btk = st.number_input("TP - Tenaga Kerja (%)", 0, 100, 50) / 100
            tp_bop = st.number_input("TP - Overhead (%)", 0, 100, 50) / 100
            
            st.info("💡 Pastikan TP Tenaga Kerja dan Overhead sesuai dengan laporan produksi lapangan.")

    if st.button("🚀 HITUNG ALOKASI BIAYA SEKARANG"):
        # Logika Perhitungan
        ue_bbb, ue_bbp = jadi + (pdp * tp_bbb), jadi + (pdp * tp_bbp)
        ue_btk, ue_bop = jadi + (pdp * tp_btk), jadi + (pdp * tp_bop)
        
        u_bbb = bbb/ue_bbb if ue_bbb>0 else 0
        u_bbp = bbp/ue_bbp if ue_bbp>0 else 0
        u_btk = btk/ue_btk if ue_btk>0 else 0
        u_bop = bop/ue_bop if ue_bop>0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        
        h_jadi = jadi * total_u
        h_pdp = (pdp*tp_bbb*u_bbb) + (pdp*tp_bbp*u_bbp) + (pdp*tp_btk*u_btk) + (pdp*tp_bop*u_bop)

        st.markdown("### 📋 Laporan Hasil Analisis")
        
        # Tampilan Hasil yang Sangat Berbeda & Menarik
        res1, res2 = st.columns([1.5, 1])
        
        with res1:
            st.markdown(f"""
            <div class="result-card bg-jadi">
                <p style="margin:0; font-size:16px;">TOTAL HPP PRODUK JADI</p>
                <h2 style="margin:0; color:white;">{format_rp(h_jadi)}</h2>
            </div>
            <div class="result-card bg-pdp">
                <p style="margin:0; font-size:16px;">TOTAL HPP PDP AKHIR</p>










