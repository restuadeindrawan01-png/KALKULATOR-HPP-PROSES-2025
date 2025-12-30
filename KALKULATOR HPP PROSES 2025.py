import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator HPP Akuntansi", page_icon="📊", layout="wide")

# --- 1. INISIALISASI SESSION STATE ---
if 'data_hpp' not in st.session_state:
    st.session_state.data_hpp = {
        'total_u': 0, 
        'h_jadi': 0, 
        'h_pdp': 0, 
        'total_akumulasi': 0, 
        'unit_jadi': 0
    }

# --- STYLE CSS: PREMIUM DARK MODE ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A !important; }
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3, h4, p, label, .stMarkdown { color: #E0E1DD !important; font-family: 'Inter', sans-serif; }

    /* --- SEMBUNYIKAN ATRIBUT STREAMLIT --- */
    #MainMenu {visibility: hidden;} /* Menu Hamburger */
    header {visibility: hidden;}    /* Header */
    footer {visibility: hidden;}    /* Footer */
  
    .card-output {
        padding: 35px;
        border-radius: 20px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .blue-grad { background: linear-gradient(135deg, #1d3557 0%, #457b9d 100%); }
    .green-grad { background: linear-gradient(135deg, #344e41 0%, #588157 100%); }
    .yelow-grad { background: linear-gradient(135deg, #b8860b 0%, #daa520 100%); }
    .gold-grad { background: linear-gradient(135deg, #434343 0%, #000000 100%); border: 1px solid #daa520; }

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

    .stButton>button { 
        background: linear-gradient(90deg, #415A77 0%, #778DA9 100%);
        color: white; border-radius: 15px; width: 100%; font-weight: bold; 
        height: 65px; font-size: 22px; border: none; margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stButton>button:hover { background: #E0E1DD; color: #0D1B2A; transform: scale(1.01); }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI FORMATTING (SOLUSI KESALAHAN) ---
def format_bersih(angka):
    """Menghilangkan .0 dan memberi titik pemisah ribuan"""
    return f"{int(angka):,}".replace(",", ".")
    
def format_rp(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- NAVIGASI HEADER ---
c_head, c_nav = st.columns([2.5, 1.5])
with c_head:
    st.markdown("# 📊 SISTEM AKUNTANSI BIAYA")
with c_nav:
    menu = st.selectbox("", ["🏠 Dashboard", "🏭 Perhitungan HPP", "💰 Analisis Profitabilitas"], label_visibility="collapsed")
    st.markdown(f'<p style="text-align:right; color:#778DA9; font-size:13px; margin-top:-10px;">Menu Aktif: {menu}</p>', unsafe_allow_html=True)

st.divider()

# --- HALAMAN DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("## 👋 Selamat Datang di Dashboard Utama")
    st.write("Sistem Informasi Akuntansi Biaya membantu anda dalam melakukan Perhitungan Harga Pokok produksi secara otomatis.")
    
    # KOREKSI: Memperbaiki string literal dan indentasi expander
    with st.expander("🔵 Akurasi Data"):
        st.info("""*Akurasi Tinggi:* Sistem menggunakan rumus Unit Ekuivalen yang presisi untuk memisahkan biaya produk jadi dan PDP. 
        Data biaya diakumulasikan berdasarkan tingkat penyelesaian (PDP), memastikan tidak ada 
        biaya yang tumpang tindih antara produk jadi dan produk dalam proses.""")
        
    with st.expander("🟢 Efisiensi Biaya"):
        st.success("""*Optimalisasi Anggaran:* Mempermudah dalam Pemantauan elemen produksi secara mendetail seperti; distribusi biaya Bahan Baku (BBB), Bahan Penolong (BBP), 
        Tenaga Kerja (BTK), hingga Overhead (BOP). Dengan mengetahui biaya per unit secara detail, 
        perusahaan dapat melakukan efisiensi pada pos biaya yang membengkak.""")
        
    with st.expander("🟡 Laporan Otomatis"):
        st.warning("""*Kecepatan Analisis:* Membantu mempermudah dan mempersingkat, dari perhitungan manual yang rumit. Cukup masukkan data produksi 
        dan persentase penyelesaian, sistem akan menyajikan laporan HPP dan nilai persediaan PDP 
        secara instan dalam hitungan detik.""")     
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/data-report-concept-illustration_114360-883.jpg", use_container_width=True)
            
# --- HALAMAN PERHITUNGAN HPP ---
elif menu == "🏭 Perhitungan HPP":
    st.markdown("### ⚙️ Konfigurasi Biaya & Data Produksi")
    c1, c2, c3 = st.columns(3, gap="large")
    
    with c1:
        st.markdown('<div class="input-box">', unsafe_allow_html=True)
        st.markdown("#### 📦 Volume Unit")
        st.image("https://cdn-icons-png.flaticon.com/512/5164/5164023.png", width=60)
        jadi = st.number_input("Unit Selesai (Jadi)", min_value=0, step=1)
        pdp = st.number_input("Unit Belum Selesai (PDP)", min_value=0, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="input-box">', unsafe_allow_html=True)
        st.markdown("#### 💰 Alokasi Biaya")
        st.image("https://cdn-icons-png.flaticon.com/512/2454/2454282.png", width=60)
        bbb = st.number_input("Biaya Bahan Baku", min_value=0)
        bbp = st.number_input("Biaya Bahan Penolong", min_value=0)
        btk = st.number_input("Biaya Tenaga Kerja", min_value=0)
        bop = st.number_input("Biaya Overhead", min_value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="input-box">', unsafe_allow_html=True)
        st.markdown("#### 📈 Progress PDP (%)")
        st.image("https://cdn-icons-png.flaticon.com/512/1548/1548914.png", width=60)
        tp_bbb = st.number_input("Penyelesaian BBB (%)", 0, 100, 100) / 100
        tp_bbp = st.number_input("Penyelesaian BBP (%)", 0, 100, 100) / 100
        tp_btk = st.number_input("Penyelesaian BTK (%)", 0, 100, 50) / 100
        tp_bop = st.number_input("Penyelesaian BOP (%)", 0, 100, 50) / 100
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 HITUNG HPP SEKARANG"):
        ue_bbb, ue_bbp = jadi + (pdp * tp_bbb), jadi + (pdp * tp_bbp)
        ue_btk, ue_bop = jadi + (pdp * tp_btk), jadi + (pdp * tp_bop)
        
        u_bbb = bbb/ue_bbb if ue_bbb > 0 else 0
        u_bbp = bbp/ue_bbp if ue_bbp > 0 else 0
        u_btk = btk/ue_btk if ue_btk > 0 else 0
        u_bop = bop/ue_bop if ue_bop > 0 else 0
        total_u = u_bbb + u_bbp + u_btk + u_bop
        
        h_jadi = jadi * total_u
        h_pdp = (pdp*tp_bbb*u_bbb) + (pdp*tp_bbp*u_bbp) + (pdp*tp_btk*u_btk) + (pdp*tp_bop*u_bop)

        # Simpan ke Session State
        st.session_state.data_hpp = {
            'total_u': total_u, 
            'h_jadi': h_jadi, 
            'h_pdp': h_pdp, 
            'unit_jadi': jadi
        }

        st.divider()
        st.markdown("### 📋 Hasil Perhitungan HPP")
        res_l, res_r = st.columns([1.8, 1], gap="medium")
        
        with res_l:
            st.markdown(f"""
                <div class="card-output blue-grad">
                    <p style="margin:0; opacity:0.8;">HPP PRODUK JADI </p>
                    <h1 style="margin:0; font-size:50px;">{format_rp(h_jadi)}</h1>
                </div>
                <div class="card-output green-grad">
                    <p style="margin:0; opacity:0.8;">HPP PRODUK DALAM PROSES (PDP)</p>
                    <h1 style="margin:0; font-size:50px;">{format_rp(h_pdp)}</h1>
                </div>
                <div class="card-output yelow-grad">
                    <p style="margin:0; opacity:0.8;">JUMLAH BIAYA PRODUKSI (TOTAL)</p>
                    <h1 style="margin:0; font-size:50px;">{format_rp(h_jadi + h_pdp)}</h1>
                </div>
            """, unsafe_allow_html=True)
            st.metric("Total Biaya Per Unit Produksi", format_rp(total_u))

        with res_r:
            st.markdown("#### 📏 Unit Ekuivalen")
            for l, v in [("BBB", ue_bbb), ("BBP", ue_bbp), ("BTK", ue_btk), ("BOP", ue_bop)]:
                st.markdown(f'<div class="ue-modern"><span>UE {l}</span><span class="ue-val">{format_bersih(v)}</span></div>', unsafe_allow_html=True)
        
        with st.expander("🔍 Lihat Rincian Langkah-Langkah"):
            st.markdown("#### 1. Unit Ekuivalen (UE)")
            st.write(f"BBB: {jadi} + ({pdp} * {int(tp_bbb*100)}%) = *{format_bersih(ue_bbb)}*")
            st.write(f"BBP: {jadi} + ({pdp} * {int(tp_bbp*100)}%) = *{format_bersih(ue_bbp)}*")
            st.write(f"BTK: {jadi} + ({pdp} * {int(tp_btk*100)}%) = *{format_bersih(ue_btk)}*")
            st.write(f"BOP: {jadi} + ({pdp} * {int(tp_bop*100)}%) = *{format_bersih(ue_bop)}*")
            st.write(f"*Total Unit Ekuivalen: {format_bersih(ue_bbb + ue_bbp + ue_btk + ue_bop)}*")
            
            st.markdown("#### 2. Biaya Per Unit")
            st.write(f"BBB: {format_bersih(bbb)} / {format_bersih(ue_bbb)} = *Rp {format_bersih(u_bbb)}*")
            st.write(f"BBP: {format_bersih(bbp)} / {format_bersih(ue_bbp)} = *Rp {format_bersih(u_bbp)}*")
            st.write(f"BTK: {format_bersih(btk)} / {format_bersih(ue_btk)} = *Rp {format_bersih(u_btk)}*")
            st.write(f"BOP: {format_bersih(bop)} / {format_bersih(ue_bop)} = *Rp {format_bersih(u_bop)}*")
            st.write(f"*Total Biaya Per Unit: Rp {format_bersih(total_u)}*")
            
            st.markdown("#### 3. Alokasi ke PDP")
            st.write(f"BBB: {pdp} * {int(tp_bbb*100)}% * Rp {format_bersih(u_bbb)} = *Rp {format_bersih(pdp*tp_bbb*u_bbb)}*")
            st.write(f"BBP: {pdp} * {int(tp_bbp*100)}% * Rp {format_bersih(u_bbp)} = *Rp {format_bersih(pdp*tp_bbp*u_bbp)}*")
            st.write(f"BTK: {pdp} * {int(tp_btk*100)}% * Rp {format_bersih(u_btk)} = *Rp {format_bersih(pdp*tp_btk*u_btk)}*")
            st.write(f"BOP: {pdp} * {int(tp_bop*100)}% * Rp {format_bersih(u_bop)} = *Rp {format_bersih(pdp*tp_bop*u_bop)}*")
            st.write(f"*Total Nilai PDP: Rp {format_bersih(h_pdp)}*")
                     
        st.success("✅ Data berhasil disimpan! Buka menu 'Analisis Profitabilitas' untuk melihat laba.")

# --- 3. HALAMAN ANALISIS PROFITABILITAS ---
elif menu == "💰 Analisis Profitabilitas":
    st.markdown("### 📈 Ikhtisar Harga Jual & Laba Rugi")
    
    if st.session_state.data_hpp['total_u'] == 0:
        st.warning("⚠️ Harap lakukan 'Perhitungan HPP' terlebih dahulu sebelum mengakses halaman ini.")
    else:
        col_input1, col_input2 = st.columns([1, 2])
        with col_input1:
            st.markdown("#### 🏷️ Penetapan Harga")
            harga_jual = st.number_input("Masukkan Harga Jual per Unit (Rp)", min_value=0, step=1000)
        
        total_u = st.session_state.data_hpp['total_u']
        unit_jadi = st.session_state.data_hpp['unit_jadi']
        
        laba_per_unit = harga_jual - total_u
        total_laba = laba_per_unit * unit_jadi
        margin_pct = (laba_per_unit / harga_jual * 100) if harga_jual > 0 else 0
        
        # --- PERBAIKAN INDENTASI PADA BAGIAN METRIC ---
        st.divider()
        c_res1, c_res2, c_res3 = st.columns(3)
        
        with c_res1:
            # Menampilkan modal dengan detail 4 desimal
            st.metric("Modal per Unit (HPP)", f"Rp {total_u:,.4f}".replace(",", "X").replace(".", ",").replace("X", "."))

        with c_res2:
            # Menampilkan persentase desimal lebih panjang (4 angka di belakang koma)
            st.metric(
                "Laba/Rugi per Unit", 
                f"Rp {laba_per_unit:,.4f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                delta=f"{margin_pct:.4f}% Margin"
            )

        with c_res3:
            # Menampilkan Total Laba Bersih dengan detail desimal
            st.metric("Total Laba Bersih", f"Rp {total_laba:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        st.markdown(f"""
            <div class="card-output gold-grad">
                <p style="margin:0; opacity:0.8; font-size:16px;">PROYEKSI TOTAL PENDAPATAN (REVENUE)</p>
                <h1 style="margin:0; font-size:55px;">{format_rp(harga_jual * unit_jadi)}</h1>
                <p style="margin-top:10px; font-size:14px;">Berdasarkan {unit_jadi} unit selesai</p>
            </div>
        """, unsafe_allow_html=True)

        # SEKSI BARU: PERINCIAN PERHITUNGAN
        with st.expander("📑 Lihat Perincian Perhitungan Profitabilitas"):
            st.markdown("#### 🧮 Rumus & Langkah Perhitungan")
            
            st.markdown("*1. Laba/Rugi per Unit*")
            st.write(f"Harga Jual ({format_rp(harga_jual)}) - Modal per Unit ({format_rp(total_u)}) = *{format_rp(laba_per_unit)}*")
            
            st.markdown("*2. Margin Keuntungan (%)*")
            st.write(f"(Laba per Unit ({format_rp(laba_per_unit)}) / Harga Jual ({format_rp(harga_jual)})) * 100% = *{margin_pct:.2f}%*")
            
            st.markdown("*3. Total Pendapatan (Revenue)*")
            st.write(f"Harga Jual ({format_rp(harga_jual)}) * Jumlah Unit Jadi ({format_bersih(unit_jadi)}) = *{format_rp(revenue)}*")
            
            st.markdown("*4. Total Laba Bersih*")
            st.write(f"Laba per Unit ({format_rp(laba_per_unit)}) * Jumlah Unit Jadi ({format_bersih(unit_jadi)}) = *{format_rp(total_laba)}*")
            
        if harga_jual > 0:
            if laba_per_unit < 0:
                st.error("🚨 PERINGATAN: Harga jual berada di bawah biaya produksi (RUGI).")
            elif laba_per_unit > 0:
                st.success(f"✅ Strategi harga aman. Anda mendapatkan margin sebesar {format_rp(laba_per_unit)} per produk.")





































