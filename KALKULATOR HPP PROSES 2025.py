import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS (TAMPILAN MODERN & BERJARAK) ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A !important; }
    h1, h2, h3, p, label { color: #E0E1DD !important; }
    
    /* Memberi jarak pada input angka */
    .stNumberInput { margin-bottom: 20px !important; }
    
    /* Box Hasil Perhitungan */
    .card-hasil {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .bg-biru { background-color: #1B263B; border-left: 8px solid #415A77; }
    .bg-hijau { background-color: #1B263B; border-left: 8px solid #588157; }

    /* Rincian Vertikal Unit Ekuivalen */
    .ue-box {
        background-color: #1B263B;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #415A77;
    }
    </style>
""", unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- NAVIGASI ---
st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")
menu = st.tabs(["🏠 Dashboard", "🏭 Hitung HPP"])

# --- HALAMAN DASHBOARD ---
with menu[0]:
    st.markdown("### 👋 Selamat Datang")
    st.info("Gunakan tab 'Hitung HPP' di atas untuk memulai simulasi biaya produksi.")
    st.image("https://img.freepik.com/free-vector/data-report-concept-illustration_114360-883.jpg", width=500)

# --- HALAMAN PERHITUNGAN ---
with menu[1]:
    st.markdown("### 📝 Input Data Produksi & Biaya")
    
    # Membuat 3 kolom agar tidak terlalu rapat
    col1, col_space, col2 = st.columns([1, 0.1, 1])
    
    with col1:
        st.subheader("1. Data Unit")
        unit_jadi = st.number_input("Unit Produk Jadi", min_value=0, step=1)
        unit_pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1)
        
        st.markdown("---")
        st.subheader("2. Total Biaya Produksi")
        c_bbb = st.number_input("Biaya Bahan Baku (BBB)", min_value=0)
        c_bbp = st.number_input("Biaya Bahan Penolong (BBP)", min_value=0)
        c_btk = st.number_input("Biaya Tenaga Kerja (BTKL)", min_value=0)
        c_bop = st.number_input("Biaya Overhead (BOP)", min_value=0)

    with col2:
        st.subheader("3. Tingkat Penyelesaian (%)")
        tp_bbb = st.number_input("TP - Bahan Baku (%)", 0, 100, 100) / 100
        tp_bbp = st.number_input("TP - Bahan Penolong (%)", 0, 100, 100) / 100
        tp_btk = st.number_input("TP - Tenaga Kerja (%)", 0, 100, 50) / 100
        tp_bop = st.number_input("TP - Overhead (%)", 0, 100, 50) / 100
        st.warning("💡 Masukkan persentase kemajuan produksi.")

    if st.button("🚀 PROSES ALOKASI BIAYA"):
        # Hitung Unit Ekuivalen
        ue_bbb = unit_jadi + (unit_pdp * tp_bbb)
        ue_bbp = unit_jadi + (unit_pdp * tp_bbp)
        ue_btk = unit_jadi + (unit_pdp * tp_btk)
        ue_bop = unit_jadi + (unit_pdp * tp_bop)
        
        # Biaya Per Unit
        u_bbb = c_bbb / ue_bbb if ue_bbb > 0 else 0
        u_bbp = c_bbp / ue_bbp if ue_bbp > 0 else 0
        u_btk = c_btk / ue_btk if ue_btk > 0 else 0
        u_bop = c_bop / ue_bop if ue_bop > 0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        
        # Hasil Akhir
        hpp_jadi = unit_jadi * total_u
        hpp_pdp = (unit_pdp*tp_bbb*u_bbb) + (unit_pdp*tp_bbp*u_bbp) + (unit_pdp*tp_btk*u_btk) + (unit_pdp*tp_bop*u_bop)

        st.divider()
        st.subheader("📋 Laporan Alokasi Biaya")
        
        res1, res2 = st.columns([1.5, 1])
        
        with res1:
            st.markdown(f"""
                <div class="card-hasil bg-biru">
                    <small>TOTAL HPP PRODUK JADI</small>
                    <h2>{format_rp(hpp_jadi)}</h2>
                </div>
                <div class="card-hasil bg-hijau">
                    <small>TOTAL HPP PDP AKHIR</small>
                    <h2>{format_rp(hpp_pdp)}</h2>
                </div>
            """, unsafe_allow_html=True)
            st.metric("Total Biaya Per Unit", format_rp(total_u))

        with res2:
            st.markdown("#### 📏 Rincian UE (Vertikal)")
            for lab, val in [("BBB", ue_bbb), ("BBP", ue_bbp), ("BTK", ue_btk), ("BOP", ue_bop)]:
                st.markdown(f"""<div class="ue-box"><small>UE {lab}</small><br><b>{val:,.1f} Unit</b></div>""", unsafe_allow_html=True)











