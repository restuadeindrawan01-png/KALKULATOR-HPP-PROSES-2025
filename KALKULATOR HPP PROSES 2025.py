import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- STYLE CSS: THEME BIRU TUA & INTERAKTIF DASHBOARD ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, p, label, .stMarkdown { color: #E0E1DD !important; }
    
    /* Styling khusus untuk konten yang bisa dibuka (Expander) */
    .st-emotion-cache-p5mtre { background-color: #1B263B !important; border: 1px solid #415A77 !important; border-radius: 10px; }
    
    /* Tombol Navigasi & Hitung */
    .stButton>button { background-color: #415A77; color: white; border-radius: 8px; width: 100%; border: 1px solid #778DA9; }
    .stNumberInput input { background-color: #FFFFFF !important; color: #0D1B2A !important; font-weight: bold; }
    
    /* Warna spesifik untuk kartu dashboard */
    .card-blue { border-left: 10px solid #A2D2FF; }
    .card-green { border-left: 10px solid #B2D8B2; }
    .card-yellow { border-left: 10px solid #E9EDC9; }
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

# --- HALAMAN 1: DASHBOARD (DENGAN MENU YANG BISA DIBUKA) ---
if menu == "🏠 Dashboard Utama":
    st.markdown("### Dashboard Kinerja Produksi")
    st.write("Klik pada menu di bawah ini untuk melihat detail informasi:")

    # Menu Akurasi Data
    with st.expander("🔵 Akurasi Data (Klik untuk detail)"):
        st.markdown("""
        <div class='card-blue' style='padding:10px;'>
        <strong>Standar PSAK:</strong> Perhitungan ini mengikuti Pernyataan Standar Akuntansi Keuangan untuk memastikan validitas laporan laba rugi.
        <br><em>Manfaat: Menghindari kesalahan pencatatan aset persediaan.</em>
        </div>
        """, unsafe_allow_html=True)

    # Menu Efisiensi Biaya
    with st.expander("🟢 Efisiensi Biaya (Klik untuk detail)"):
        st.markdown("""
        <div class='card-green' style='padding:10px;'>
        <strong>Kontrol PDP:</strong> Memantau alokasi biaya pada Produk Dalam Proses (PDP) agar tidak terjadi pemborosan bahan baku atau tenaga kerja.
        <br><em>Target: Menurunkan biaya overhead yang tidak perlu.</em>
        </div>
        """, unsafe_allow_html=True)

    # Menu Laporan Otomatis
    with st.expander("🟡 Laporan Otomatis (Klik untuk detail)"):
        st.markdown("""
        <div class='card-yellow' style='padding:10px;'>
        <strong>Kecepatan Hitung:</strong> Unit ekuivalen dan biaya per unit dihitung secara real-time tanpa perlu rumus manual di spreadsheet.
        <br><em>Fitur: Rincian biaya per unsur (BBB, BTK, BOP).</em>
        </div>
        """, unsafe_allow_html=True)

    st.image("https://img.freepik.com/free-vector/accounting-concept-illustration_114360-1532.jpg", use_container_width=True)

# --- HALAMAN 2: KALKULATOR HPP (RINCIAN LENGKAP) ---
elif menu == "🏭 Kalkulator HPP":
    st.subheader("🏭 Form Perhitungan & Laporan HPP")
    
    # Input
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 1. Data Unit")
        jadi = st.number_input("Unit Produk Jadi", min_value=0, step=1)
        pdp = st.number_input("Unit PDP Akhir", min_value=0, step=1)
    with c2:
        st.markdown("### 2. Total Biaya")
        c_bbb = st.number_input("Total Biaya Bahan Baku (BBB)", min_value=0, step=1000)
        c_bk = st.number_input("Total Biaya Konversi (BTK + BOP)", min_value=0, step=1000)

    st.markdown("### 3. Tingkat Penyelesaian (%)")
    t1, t2 = st.columns(2)
    tp_bbb = t1.number_input("TP Bahan Baku (%)", 0, 100, 100) / 100
    tp_bk = t2.number_input("TP Biaya Konversi (%)", 0, 100, 50) / 100

    if st.button("🚀 JALANKAN PERHITUNGAN"):
        # Hitung UE & Biaya/Unit
        ue_bbb = jadi + (pdp * tp_bbb)
        ue_bk = jadi + (pdp * tp_bk)
        u_bbb = c_bbb / ue_bbb if ue_bbb > 0 else 0
        u_bk = c_bk / ue_bk if ue_bk > 0 else 0
        total_u = u_bbb + u_bk
        
        # Alokasi
        hpp_jadi = jadi * total_u
        hpp_pdp = (pdp * tp_bbb * u_bbb) + (pdp * tp_bk * u_bk)

        # --- LAPORAN HASIL RINCI ---
        st.markdown("### 📋 Laporan Hasil Perhitungan")
        res1, res2, res3 = st.columns(3)
        res1.metric("UE Bahan Baku", f"{ue_bbb} Unit")
        res2.metric("UE Konversi", f"{ue_bk} Unit")
        res3.metric("Biaya/Unit Total", format_rp(total_u))

        st.success(f"*Harga Pokok Produk Jadi: {format_rp(hpp_jadi)}*")
        st.warning(f"*Harga Pokok PDP Akhir: {format_rp(hpp_pdp)}*")

        # Rincian Rumus
        with st.expander("📚 Lihat Rincian Rumus Akuntansi"):
            st.latex(r"UE = \text{Jadi} + (\text{PDP} \times \text{TP}\%)")
            st.latex(r"\text{Biaya/Unit} = \frac{\text{Total Biaya}}{\text{Unit Ekuivalen}}")
            st.info("Perhitungan ini menggunakan Metode Harga Pokok Rata-rata Tertimbang.")





