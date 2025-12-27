import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- SEMBUNYIKAN MENU STREAMLIT ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {angka:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("📊 SISTEM AKUNTANSI BIAYA")
st.info("Pilih metode perhitungan pada tab di bawah ini.")

tab1, tab2 = st.tabs(["📋 Job Order Costing", "🏭 Process Costing"])

# --- METODE JOB ORDER COSTING ---
with tab1:
    st.header("Metode Harga Pokok Pesanan")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Biaya")
        nama = st.text_input("Nama Pesanan", placeholder="Contoh: Pesanan Meja Kantor")
        bbb = st.number_input("Biaya Bahan Baku", min_value=0.0, step=1000.0)
        bbp = st.number_input("Biaya Bahan Penolong (Job)", min_value=0.0, step=1000.0)
        btkl = st.number_input("Biaya Tenaga Kerja Langsung", min_value=0.0, step=1000.0)
        bop = st.number_input("Biaya Overhead Pabrik (BOP)", min_value=0.0, step=1000.0)

    with col2:
        st.subheader("Hasil Perhitungan")
        if st.button("HITUNG HPP PESANAN"):
            total_hpp = bbb + bbp + btkl + bop
            st.success(f"Pesanan: {nama}")
            st.metric("Total HPP Pesanan", format_rp(total_hpp))
            
            with st.expander("Lihat Rumus"):
                st.latex(r"HPP = BBB + BBP + BTKL + BOP")

# --- METODE PROCESS COSTING ---
with tab2:
    st.header("Metode Harga Pokok Proses")
    
    with st.container():
        st.subheader("1. Data Produksi")
        c1, c2, c3 = st.columns(3)
        produk_jadi = c1.number_input("Produk Selesai (Unit)", min_value=0.0, key="jadi")
        produk_pdp = c2.number_input("Produk Dalam Proses (Unit)", min_value=0.0, key="pdp")
        
        st.subheader("2. Input Biaya Produksi")
        b1, b2, b3, b4 = st.columns(4)
        cost_bbb = b1.number_input("Total Biaya Bahan Baku", min_value=0.0, step=1000.0)
        cost_bbp = b2.number_input("Total Biaya Penolong", min_value=0.0, step=1000.0)
        cost_btk = b3.number_input("Total Biaya Tenaga Kerja", min_value=0.0, step=1000.0)
        cost_bop = b4.number_input("Total Biaya BOP", min_value=0.0, step=1000.0)

        st.subheader("3. Tingkat Penyelesaian (%)")
        t1, t2, t3, t4 = st.columns(4)
        tp_bbb = t1.slider("TP Bahan Baku", 0, 100, 100) / 100
        tp_bbp = t2.slider("TP Bahan Penolong", 0, 100, 100) / 100
        tp_btk = t3.slider("TP Tenaga Kerja", 0, 100, 50) / 100
        tp_bop = t4.slider("TP BOP", 0, 100, 50) / 100

    if st.button("PROSES PERHITUNGAN BIAYA"):
        # Hitung Unit Ekuivalen (UE)
        ue_bbb = produk_jadi + (produk_pdp * tp_bbb)
        ue_bbp = produk_jadi + (produk_pdp * tp_bbp)
        ue_btk = produk_jadi + (produk_pdp * tp_btk)
        ue_bop = produk_jadi + (produk_pdp * tp_bop)
        
        # Hitung Biaya Per Unit
        unit_cost_bbb = cost_bbb / ue_bbb if ue_bbb > 0 else 0
        unit_cost_bbp = cost_bbp / ue_bbp if ue_bbp > 0 else 0
        unit_cost_btk = cost_btk / ue_btk if ue_btk > 0 else 0
        unit_cost_bop = cost_bop / ue_bop if ue_bop > 0 else 0
        total_unit_cost = unit_cost_bbb + unit_cost_bbp + unit_cost_btk + unit_cost_bop
        
        # Hitung Alokasi Biaya
        hpp_jadi = produk_jadi * total_unit_cost
        hpp_pdp = (produk_pdp * tp_bbb * unit_cost_bbb) + \
                  (produk_pdp * tp_bbp * unit_cost_bbp) + \
                  (produk_pdp * tp_btk * unit_cost_btk) + \
                  (produk_pdp * tp_bop * unit_cost_bop)

        st.divider()
        st.subheader("Hasil Laporan Biaya Produksi")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.info(f"Total Biaya Produksi: {format_rp(cost_bbb + cost_bbp + cost_btk + cost_bop)}")
            st.write(f"*Unit Ekuivalen:*")
            st.write(f"- BBB: {ue_bbb} unit")
            st.write(f"- BBP: {ue_bbp} unit")
            st.write(f"- BTK: {ue_btk} unit")
            st.write(f"- BOP: {ue_bop} unit")

        with col_res2:
            st.success(f"HPP Produk Jadi: {format_rp(hpp_jadi)}")
            st.warning(f"HPP Produk Dalam Proses: {format_rp(hpp_pdp)}")
            st.metric("Total Biaya Per Unit", format_rp(total_unit_cost))

        with st.expander("Lihat Rumus & Logika"):
            st.write("*Unit Ekuivalen (UE):*")
            st.latex(r"UE = Jadi + (PDP \times \% TP)")
            st.write("*Biaya per Unit:*")
            st.latex(r"Biaya/Unit = \frac{Total Biaya Unsur}{UE Unsur}")