import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import joblib
import io
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
#  KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Prediksi Pengunjung Kun Gerit",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Font ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

/* ── Root Colors ── */
:root {
    --orange:  #E67514;
    --dark:    #212121;
    --green:   #06923E;
    --mint:    #D3ECCD;
    --white:   #FFFFFF;
    --bg:      #F5F9F4;
    --card-bg: #FFFFFF;
    --border:  #D3ECCD;
    --text:    #212121;
    --muted:   #6B7280;
    --shadow:  0 4px 24px rgba(6,146,62,0.10);
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    color: var(--text);
}
.stApp {
    background: var(--bg);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--dark) !important;
    border-right: 3px solid var(--orange);
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #FFFFFF !important;
    font-weight: 500;
    padding: 6px 0;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
}

/* ── Header Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #212121 0%, #06923E 60%, #E67514 100%);
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(6,146,62,0.25);
}
.hero-banner::before {
    content: "🌿";
    position: absolute;
    right: 32px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 80px;
    opacity: 0.18;
}
.hero-banner h1 {
    color: #FFFFFF !important;
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    margin: 0 0 6px 0 !important;
    line-height: 1.2;
}
.hero-banner p {
    color: #D3ECCD !important;
    font-size: 0.95rem;
    margin: 0;
    opacity: 0.92;
}
.hero-badge {
    display: inline-block;
    background: var(--orange);
    color: white !important;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Section Title ── */
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--dark);
    margin: 0 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: "";
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, var(--green), transparent);
    border-radius: 2px;
}

/* ── Cards ── */
.card {
    background: var(--card-bg);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 18px;
    border: 1.5px solid var(--border);
    box-shadow: var(--shadow);
}
.card-accent {
    border-left: 4px solid var(--orange);
}
.card-green {
    border-left: 4px solid var(--green);
}

/* ── Result Box ── */
.result-box {
    background: linear-gradient(135deg, var(--green), #04712F);
    border-radius: 16px;
    padding: 28px 32px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(6,146,62,0.28);
    margin: 20px 0;
}
.result-box .result-number {
    font-size: 3rem;
    font-weight: 800;
    color: white;
    line-height: 1;
    display: block;
}
.result-box .result-label {
    color: #D3ECCD;
    font-size: 0.9rem;
    margin-top: 6px;
    display: block;
}
.result-box .result-spot {
    color: #FFFFFF;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 10px;
    display: block;
}

/* ── Info Chips ── */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
}
.chip {
    background: var(--mint);
    color: var(--dark);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.chip-orange {
    background: #FEE9D7;
    color: var(--orange);
}
.chip-green {
    background: var(--mint);
    color: var(--green);
}

/* ── Metric Cards ── */
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1.5px solid var(--border);
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.metric-card .metric-value {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--green);
    display: block;
}
.metric-card .metric-label {
    font-size: 0.75rem;
    color: var(--muted);
    font-weight: 500;
    margin-top: 2px;
    display: block;
}

/* ── Table ── */
.dataframe-container {
    border-radius: 12px;
    overflow: hidden;
    border: 1.5px solid var(--border);
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
}

/* ── Form inputs ── */
.stSelectbox [data-baseweb="select"] {
    border-radius: 10px !important;
}
.stNumberInput input {
    border-radius: 10px !important;
}
.stSlider [data-baseweb="slider"] {
    color: var(--green) !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 20px 0 !important;
}

/* ── Alert boxes ── */
.stAlert {
    border-radius: 12px !important;
}

/* ── Tab Styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--mint);
    border-radius: 12px;
    padding: 5px 6px;
    gap: 6px;
    margin-bottom: 24px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 600 !important;
    color: var(--dark) !important;
    padding: 10px 22px !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.2px;
}
.stTabs [aria-selected="true"] {
    background: var(--green) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 8px !important;
}

/* ── Download buttons ── */
.download-area {
    background: #F5F9F4;
    border: 1.5px dashed var(--green);
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 12px;
}

/* ── Sidebar Logo ── */
.sidebar-logo {
    text-align: center;
    padding: 16px 0 24px 0;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 20px;
}
.sidebar-logo .logo-icon {
    font-size: 48px;
    display: block;
    margin-bottom: 6px;
}
.sidebar-logo .logo-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #E67514 !important;
    letter-spacing: 0.5px;
}
.sidebar-logo .logo-sub {
    font-size: 0.7rem;
    color: #D3ECCD !important;
    opacity: 0.8;
}

/* Tooltip hint */
.hint-text {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: -8px;
    margin-bottom: 8px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--mint); border-radius: 3px; }
::-webkit-scrollbar-thumb { background: var(--green); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  LOAD MODEL & ARTEFAK
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

@st.cache_resource
def load_artifacts():
    model  = joblib.load(os.path.join(MODELS_DIR, "lasso_model.pkl"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    le     = joblib.load(os.path.join(MODELS_DIR, "le_spot.pkl"))
    return model, scaler, le

model, scaler, le_spot = load_artifacts()

SPOTS = list(le_spot.classes_)
ORDINAL_MAP = {'Mudah': 0, 'Sedang': 1, 'Sukar': 2}
NAMA_BULAN = {
    1:'Januari', 2:'Februari', 3:'Maret', 4:'April',
    5:'Mei', 6:'Juni', 7:'Juli', 8:'Agustus',
    9:'September', 10:'Oktober', 11:'November', 12:'Desember'
}
FITUR = ['Nama_Spot_enc', 'Bulan', 'Event_Khusus',
         'Harga_Tiket_Log', 'Aksesibilitas_enc', 'Luas_Lahan', 'Tiket_x_Jam']


# ─────────────────────────────────────────────
#  DATABASE SQLite
# ─────────────────────────────────────────────
DB_PATH = os.path.join(BASE_DIR, "data/kun_gerit_predictions.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal         TEXT,
            nama_spot       TEXT,
            bulan           INTEGER,
            nama_bulan      TEXT,
            event_khusus    INTEGER,
            harga_tiket     INTEGER,
            jam_operasional INTEGER,
            aksesibilitas   TEXT,
            luas_lahan      INTEGER,
            tiket_x_jam     INTEGER,
            prediksi        INTEGER,
            catatan         TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_prediction(data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO predictions
        (tanggal, nama_spot, bulan, nama_bulan, event_khusus,
         harga_tiket, jam_operasional, aksesibilitas, luas_lahan,
         tiket_x_jam, prediksi, catatan)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data['tanggal'], data['nama_spot'], data['bulan'],
        data['nama_bulan'], data['event_khusus'], data['harga_tiket'],
        data['jam_operasional'], data['aksesibilitas'], data['luas_lahan'],
        data['tiket_x_jam'], data['prediksi'], data['catatan']
    ))
    conn.commit()
    conn.close()

def load_predictions() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY id DESC", conn)
    conn.close()
    return df

def delete_prediction(pred_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM predictions WHERE id = ?", (pred_id,))
    conn.commit()
    conn.close()

def clear_all_predictions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()

init_db()


# ─────────────────────────────────────────────
#  FUNGSI PREDIKSI
# ─────────────────────────────────────────────
def predict_visitors(nama_spot, bulan, event_khusus, harga_tiket,
                     jam_operasional, aksesibilitas, luas_lahan):
    spot_enc    = le_spot.transform([nama_spot])[0]
    akses_enc   = ORDINAL_MAP[aksesibilitas]
    harga_log   = np.log1p(harga_tiket)
    tiket_x_jam = harga_tiket * jam_operasional

    features = pd.DataFrame([[spot_enc, bulan, event_khusus,
                               harga_log, akses_enc, luas_lahan, tiket_x_jam]],
                             columns=FITUR)
    features_scaled = scaler.transform(features)
    pred_log = model.predict(features_scaled)[0]
    pred_actual = max(0, int(np.round(np.expm1(pred_log))))
    return pred_actual, tiket_x_jam


# ─────────────────────────────────────────────
#  FUNGSI EXPORT
# ─────────────────────────────────────────────
def df_to_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Riwayat Prediksi')
        ws = writer.sheets['Riwayat Prediksi']
        # Auto-fit kolom
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 40)
    return output.getvalue()

def df_to_pdf(df: pd.DataFrame) -> bytes:
    """Generate simple PDF report using reportlab."""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                     Paragraph, Spacer)
    from reportlab.lib.units import cm

    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=landscape(A4),
                             leftMargin=1.5*cm, rightMargin=1.5*cm,
                             topMargin=1.5*cm, bottomMargin=1.5*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title2', parent=styles['Heading1'],
                                  fontSize=14, textColor=colors.HexColor('#06923E'),
                                  spaceAfter=6)
    sub_style   = ParagraphStyle('Sub', parent=styles['Normal'],
                                  fontSize=9, textColor=colors.HexColor('#6B7280'),
                                  spaceAfter=12)
    elements = []
    elements.append(Paragraph("Laporan Riwayat Prediksi Pengunjung", title_style))
    elements.append(Paragraph(
        f"Sendang Kun Gerit — Digenerate: {datetime.now().strftime('%d %B %Y %H:%M')}",
        sub_style))

    # Pilih kolom yang rapi untuk PDF
    cols_pdf = ['id', 'tanggal', 'nama_spot', 'nama_bulan', 'event_khusus',
                'harga_tiket', 'jam_operasional', 'aksesibilitas',
                'luas_lahan', 'prediksi']
    df_pdf = df[cols_pdf].copy()
    df_pdf.columns = ['No', 'Tanggal', 'Spot', 'Bulan', 'Event',
                      'Harga Tiket', 'Jam Op.', 'Aksesibilitas',
                      'Luas (m²)', 'Prediksi']

    data = [df_pdf.columns.tolist()] + df_pdf.values.tolist()
    col_widths = [1.2*cm, 2.5*cm, 2.8*cm, 2.2*cm, 1.5*cm,
                  2.4*cm, 1.8*cm, 2.8*cm, 2.2*cm, 2.4*cm]

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#06923E')),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,0), 8),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.HexColor('#FFFFFF'), colors.HexColor('#F5F9F4')]),
        ('FONTSIZE',   (0,1), (-1,-1), 7.5),
        ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#D3ECCD')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(table)
    doc.build(elements)
    return output.getvalue()


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon"></span>
        <div class="logo-title">SENDANG KUN GERIT</div>
        <div class="logo-sub">Sistem Prediksi Pengunjung</div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigasi",
        ["Prediksi Pengunjung", "Riwayat & Dashboard"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#D3ECCD; opacity:0.7; padding: 0 8px;'>
    <b style='color:#E67514;'>Model:</b> Lasso Regression (L1)<br>
    <b style='color:#E67514;'>Fitur:</b> 7 variabel input<br>
    <b style='color:#E67514;'>Target:</b> Jumlah Pengunjung<br>
    <b style='color:#E67514;'>Transform:</b> Log1p + StandardScaler
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#aaa; padding: 0 8px;'>
    Spot Wisata:<br>
    Pemandian · Waterboom · Kuda · Villa · Pendopo · Pemancingan · Pabrik BBS
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HALAMAN 1: PREDIKSI
# ─────────────────────────────────────────────
if menu == "Prediksi Pengunjung":
    st.markdown("""
    <div class="hero-banner">
        <span class="hero-badge">AI Prediction System</span>
        <h1>Sistem Prediksi Pengunjung Per-Spot</h1>
        <p>Sendang Wisata Kun Gerit — Kukungerit, Jatibatur, Sragen</p>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_result = st.columns([1.1, 0.9], gap="large")

    with col_form:
        st.markdown('<div class="section-title">Form Input Prediksi</div>', unsafe_allow_html=True)
        # st.markdown('<div class="card card-accent">', unsafe_allow_html=True)

        # ── Spot ──
        nama_spot = st.selectbox(
            "Nama Spot Wisata",
            options=SPOTS,
            help="Pilih salah satu dari 7 spot wisata Kun Gerit"
        )

        # ── Bulan ──
        bulan_opts = {v: k for k, v in NAMA_BULAN.items()}
        bulan_nama = st.selectbox(
            "Bulan Prediksi",
            options=list(NAMA_BULAN.values()),
            help="Bulan yang akan diprediksi (1–12)"
        )
        bulan = bulan_opts[bulan_nama]

        # ── Event ──
        event_label = st.radio(
            "Adakah Event Khusus?",
            options=["Tidak Ada Event", "Ada Event Khusus"],
            horizontal=True,
            help="Event khusus (festival, liburan nasional, dll.) meningkatkan kunjungan secara signifikan"
        )
        event_khusus = 1 if event_label == "Ada Event Khusus" else 0

        col1, col2 = st.columns(2)
        with col1:
            harga_tiket = st.number_input(
                "Harga Tiket (Rp)",
                min_value=0,
                max_value=500_000,
                value=15_000,
                step=1_000,
                help="Harga tiket masuk dalam Rupiah"
            )
        with col2:
            jam_operasional = st.number_input(
                "Jam Operasional (jam/hari)",
                min_value=1,
                max_value=24,
                value=10,
                step=1,
                help="Jumlah jam buka per hari"
            )

        aksesibilitas = st.select_slider(
            "Aksesibilitas Jalan",
            options=["Mudah", "Sedang", "Sukar"],
            value="Mudah",
            help="Mudah = Dekat pintu masuk; Sedang = Sedikit jauh; Sukar = Jauh dari pintu masuk"
        )

        luas_lahan = st.number_input(
            "Luas Lahan (m²)",
            min_value=100,
            max_value=100_000,
            value=3_500,
            step=100,
            help="Total luas area spot wisata dalam meter persegi"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Catatan opsional
        catatan = st.text_input(
            "Catatan (opsional)",
            placeholder="Contoh: estimasi untuk rencana operasional Q3",
            help="Catatan untuk disimpan bersama data prediksi"
        )

        col_btn1, col_btn2 = st.columns([1.5, 1])
        with col_btn1:
            predict_btn = st.button(
                "Jalankan Prediksi",
                use_container_width=True,
                type="primary"
            )
        with col_btn2:
            save_btn = st.button(
                "Simpan Hasil",
                use_container_width=True,
                disabled=True if 'last_pred' not in st.session_state else False
            )

    # ── Kolom Kanan: Hasil ──
    with col_result:
        st.markdown('<div class="section-title">Hasil Prediksi</div>', unsafe_allow_html=True)

        if predict_btn:
            with st.spinner("Menghitung prediksi..."):
                pred_val, tiket_x_jam = predict_visitors(
                    nama_spot, bulan, event_khusus, harga_tiket,
                    jam_operasional, aksesibilitas, luas_lahan
                )

            st.session_state['last_pred'] = {
                'tanggal'        : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'nama_spot'      : nama_spot,
                'bulan'          : bulan,
                'nama_bulan'     : bulan_nama,
                'event_khusus'   : event_khusus,
                'harga_tiket'    : harga_tiket,
                'jam_operasional': jam_operasional,
                'aksesibilitas'  : aksesibilitas,
                'luas_lahan'     : luas_lahan,
                'tiket_x_jam'    : int(tiket_x_jam),
                'prediksi'       : pred_val,
                'catatan'        : catatan,
            }
            st.rerun()

        if 'last_pred' in st.session_state:
            lp = st.session_state['last_pred']

            # Event badge
            ev_badge = 'Event Khusus' if lp['event_khusus'] else 'Non-Event'
            ev_color = '#E67514' if lp['event_khusus'] else '#06923E'

            st.markdown(f"""
            <div class="result-box">
                <span class="result-spot">{lp['nama_spot']}</span>
                <span class="result-number">{lp['prediksi']:,}</span>
                <span class="result-label">Estimasi Pengunjung</span>
            </div>
            """, unsafe_allow_html=True)

            # Detail chips
            st.markdown(f"""
            <div class="chip-row">
                <span class="chip chip-green">{lp['nama_bulan']}</span>
                <span class="chip chip-orange" style="background:#FEE9D7;color:{ev_color};">{ev_badge}</span>
                <span class="chip">Rp{lp['harga_tiket']:,}</span>
                <span class="chip">{lp['jam_operasional']} jam</span>
                <span class="chip">{lp['aksesibilitas']}</span>
                <span class="chip">{lp['luas_lahan']:,} m²</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<br>', unsafe_allow_html=True)

            # Interpretasi
            if lp['prediksi'] >= 5000:
                interp = "**Sangat Ramai** — Persiapkan kapasitas & staf ekstra"
                interp_color = "#FFF0E0"
            elif lp['prediksi'] >= 3000:
                interp = "**Ramai** — Operasional normal sudah mencukupi"
                interp_color = "#FFF8E7"
            elif lp['prediksi'] >= 1500:
                interp = "**Sedang** — Kunjungan dalam kisaran normal"
                interp_color = "#FFFAE0"
            else:
                interp = "**Sepi** — Pertimbangkan promosi atau event"
                interp_color = "#F0FFF4"

            st.markdown(f"""
            <div style="background:{interp_color}; border-radius:10px; padding:12px 16px;
                        border-left: 4px solid var(--orange); margin-top:8px; font-size:0.88rem;">
                {interp}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="card" style="text-align:center; padding: 48px 24px;">
                <div style="font-size: 56px; margin-bottom: 12px;"></div>
                <div style="font-size: 1rem; font-weight: 600; color: #212121;">
                    Isi form dan klik <b>Jalankan Prediksi</b>
                </div>
                <div style="font-size: 0.82rem; color: #6B7280; margin-top: 6px;">
                    Hasil prediksi akan muncul di sini
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tombol Simpan (di luar kolom) ──
    if save_btn and 'last_pred' in st.session_state:
        save_prediction(st.session_state['last_pred'])
        st.success(f"Prediksi **{st.session_state['last_pred']['nama_spot']}** berhasil disimpan ke database!")


# ─────────────────────────────────────────────
#  HALAMAN 2: RIWAYAT & DASHBOARD
# ─────────────────────────────────────────────
elif menu == "Riwayat & Dashboard":
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import matplotlib.patches as mpatches

    st.markdown("""
    <div class="hero-banner">
        <span class="hero-badge">Analytics Dashboard</span>
        <h1>Riwayat & Dashboard Prediksi</h1>
        <p>Analisis visual & pengelolaan data hasil prediksi pengunjung Sendang Kun Gerit</p>
    </div>
    """, unsafe_allow_html=True)

    df_hist = load_predictions()

    if df_hist.empty:
        st.info("Belum ada data prediksi. Kunjungi halaman **Prediksi Pengunjung** untuk memulai.")
        st.stop()

    # ── Metric Summary ──
    st.markdown('<div class="section-title">Ringkasan Data</div>', unsafe_allow_html=True)
    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    with mc1:
        st.markdown(f"""<div class="metric-card">
            <span class="metric-value">{len(df_hist)}</span>
            <span class="metric-label">Total Prediksi</span></div>""",
            unsafe_allow_html=True)
    with mc2:
        st.markdown(f"""<div class="metric-card">
            <span class="metric-value">{df_hist['prediksi'].max():,}</span>
            <span class="metric-label">Prediksi Tertinggi</span></div>""",
            unsafe_allow_html=True)
    with mc3:
        st.markdown(f"""<div class="metric-card">
            <span class="metric-value">{int(df_hist['prediksi'].mean()):,}</span>
            <span class="metric-label">Rata-rata Prediksi</span></div>""",
            unsafe_allow_html=True)
    with mc4:
        top_spot = df_hist.groupby('nama_spot')['prediksi'].mean().idxmax()
        st.markdown(f"""<div class="metric-card">
            <span class="metric-value" style="font-size:1rem;">{top_spot}</span>
            <span class="metric-label">Spot Terpopuler</span></div>""",
            unsafe_allow_html=True)
    with mc5:
        ev_pct = df_hist['event_khusus'].mean() * 100
        st.markdown(f"""<div class="metric-card">
            <span class="metric-value">{ev_pct:.0f}%</span>
            <span class="metric-label">Prediksi dg Event</span></div>""",
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ──
    tab1, tab2, tab3 = st.tabs(["Data Riwayat", "Dashboard Grafik", "Kelola Data"])

    # ────────────────────────────
    with tab1:
        st.markdown('<div class="section-title">Tabel Riwayat Prediksi</div>', unsafe_allow_html=True)

        # Filter
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_spot = st.multiselect(
                "Filter Spot", options=df_hist['nama_spot'].unique(),
                default=list(df_hist['nama_spot'].unique())
            )
        with col_f2:
            filter_event = st.selectbox(
                "Filter Event", options=["Semua", "Event", "Non-Event"]
            )
        with col_f3:
            sort_col = st.selectbox(
                "Urutkan", options=["Terbaru", "Terlama", "Prediksi ↑", "Prediksi ↓"]
            )

        df_filtered = df_hist[df_hist['nama_spot'].isin(filter_spot)].copy()
        if filter_event == "Event":
            df_filtered = df_filtered[df_filtered['event_khusus'] == 1]
        elif filter_event == "Non-Event":
            df_filtered = df_filtered[df_filtered['event_khusus'] == 0]

        sort_map = {
            "Terbaru": ('id', False), "Terlama": ('id', True),
            "Prediksi ↑": ('prediksi', True), "Prediksi ↓": ('prediksi', False)
        }
        sc, sa = sort_map[sort_col]
        df_filtered = df_filtered.sort_values(sc, ascending=sa)

        # Tampilkan kolom ramah
        cols_show = ['id', 'tanggal', 'nama_spot', 'nama_bulan', 'event_khusus',
                     'harga_tiket', 'jam_operasional', 'aksesibilitas',
                     'luas_lahan', 'prediksi', 'catatan']
        df_display = df_filtered[cols_show].rename(columns={
            'id': 'ID_Data', 'tanggal': 'Tanggal', 'nama_spot': 'Spot',
            'nama_bulan': 'Bulan', 'event_khusus': 'No-Event(0)/Event(1)',
            'harga_tiket': 'Harga Tiket (Rp)', 'jam_operasional': 'Jam Op.',
            'aksesibilitas': 'Aksesibilitas', 'luas_lahan': 'Luas (m²)',
            'prediksi': 'Prediksi', 'catatan': 'Catatan'
        })

        st.dataframe(df_display, use_container_width=True, height=420,
                     column_config={
                         "Prediksi": st.column_config.NumberColumn(format="%d "),
                         "Harga Tiket (Rp)": st.column_config.NumberColumn(format="Rp %d"),
                     })

        st.markdown(f"*Menampilkan **{len(df_filtered)}** dari **{len(df_hist)}** total data*")

        # ── Download ──
        st.markdown('<div class="download-area">', unsafe_allow_html=True)
        st.markdown("**Unduh Data**")
        dc1, dc2 = st.columns(2)
        with dc1:
            excel_bytes = df_to_excel(df_filtered)
            st.download_button(
                "Download Excel (.xlsx)",
                data=excel_bytes,
                file_name=f"prediksi_kun_gerit_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        with dc2:
            try:
                pdf_bytes = df_to_pdf(df_filtered)
                st.download_button(
                    "Download PDF",
                    data=pdf_bytes,
                    file_name=f"laporan_prediksi_kun_gerit_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except ImportError:
                st.info("Install `reportlab` untuk export PDF: `pip install reportlab`")
        st.markdown('</div>', unsafe_allow_html=True)

    # ────────────────────────────
    with tab2:
        PALETTE = ['#06923E','#E67514','#212121','#4CAF50',
                   '#FF9800','#2196F3','#9C27B0']
        FONT_BASE = 'DejaVu Sans'

        def fig_to_png(fig) -> bytes:
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                        facecolor=fig.get_facecolor())
            buf.seek(0)
            return buf.read()

        st.markdown('<div class="section-title">Dashboard Grafik Analitik</div>', unsafe_allow_html=True)

        # ── Grafik 1: Bar prediksi per spot ──
        g1, g2 = st.columns(2)
        with g1:
            spot_avg = (df_hist.groupby('nama_spot')['prediksi']
                        .agg(['mean','max','min'])
                        .sort_values('mean', ascending=False)
                        .reset_index())

            fig1, ax1 = plt.subplots(figsize=(6, 4.2))
            fig1.patch.set_facecolor('#F5F9F4')
            ax1.set_facecolor('#F5F9F4')
            bars = ax1.bar(spot_avg['nama_spot'], spot_avg['mean'],
                           color=PALETTE[:len(spot_avg)], alpha=0.88,
                           edgecolor='white', linewidth=0.8, width=0.6)
            ax1.set_title('Rata-rata Prediksi per Spot', fontsize=11,
                          fontweight='bold', color='#212121', pad=10,
                          fontfamily=FONT_BASE)
            ax1.set_ylabel('Rata-rata Pengunjung', fontsize=9, color='#6B7280')
            ax1.tick_params(axis='x', rotation=20, labelsize=8)
            ax1.tick_params(axis='y', labelsize=8)
            ax1.yaxis.set_major_formatter(mticker.FuncFormatter(
                lambda x, _: f'{int(x):,}'))
            ax1.spines[['top','right']].set_visible(False)
            ax1.grid(axis='y', color='#E0E0E0', linewidth=0.5)
            for bar in bars:
                ax1.text(bar.get_x() + bar.get_width()/2,
                         bar.get_height() + 30,
                         f'{int(bar.get_height()):,}',
                         ha='center', va='bottom', fontsize=7.5,
                         color='#212121', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig1)
            img1 = fig_to_png(fig1)
            plt.close(fig1)
            st.download_button("Unduh Grafik 1",
                               data=img1, file_name="grafik_avg_spot.png",
                               mime="image/png", use_container_width=True)

        # ── Grafik 2: Event vs Non-Event ──
        with g2:
            ev_grp = (df_hist.groupby(['nama_spot','event_khusus'])['prediksi']
                      .mean().reset_index())
            spots_ev = ev_grp['nama_spot'].unique()
            x = np.arange(len(spots_ev))
            w = 0.35

            fig2, ax2 = plt.subplots(figsize=(6, 4.2))
            fig2.patch.set_facecolor('#F5F9F4')
            ax2.set_facecolor('#F5F9F4')

            ev0 = ev_grp[ev_grp['event_khusus']==0].set_index('nama_spot')['prediksi']
            ev1 = ev_grp[ev_grp['event_khusus']==1].set_index('nama_spot')['prediksi']

            vals0 = [ev0.get(s, 0) for s in spots_ev]
            vals1 = [ev1.get(s, 0) for s in spots_ev]

            b0 = ax2.bar(x - w/2, vals0, w, color='#06923E', alpha=0.85,
                         edgecolor='white', label='Non-Event')
            b1 = ax2.bar(x + w/2, vals1, w, color='#E67514', alpha=0.85,
                         edgecolor='white', label='Event Khusus')

            ax2.set_title('Prediksi: Event vs Non-Event per Spot', fontsize=11,
                          fontweight='bold', color='#212121', pad=10,
                          fontfamily=FONT_BASE)
            ax2.set_xticks(x)
            ax2.set_xticklabels(spots_ev, rotation=20, ha='right', fontsize=8)
            ax2.yaxis.set_major_formatter(mticker.FuncFormatter(
                lambda x, _: f'{int(x):,}'))
            ax2.tick_params(axis='y', labelsize=8)
            ax2.spines[['top','right']].set_visible(False)
            ax2.grid(axis='y', color='#E0E0E0', linewidth=0.5)
            ax2.legend(fontsize=8.5)
            plt.tight_layout()
            st.pyplot(fig2)
            img2 = fig_to_png(fig2)
            plt.close(fig2)
            st.download_button("Unduh Grafik 2",
                               data=img2, file_name="grafik_event_vs_nonevent.png",
                               mime="image/png", use_container_width=True)

        # ── Grafik 3: Tren per Bulan ──
        g3, g4 = st.columns(2)
        with g3:
            bulan_grp = (df_hist.groupby('bulan')['prediksi']
                         .mean().reset_index()
                         .sort_values('bulan'))
            bulan_grp['nama_bulan'] = bulan_grp['bulan'].map(
                {k: v[:3] for k, v in NAMA_BULAN.items()})

            fig3, ax3 = plt.subplots(figsize=(6, 4.2))
            fig3.patch.set_facecolor('#F5F9F4')
            ax3.set_facecolor('#F5F9F4')
            ax3.fill_between(bulan_grp['bulan'], bulan_grp['prediksi'],
                             alpha=0.12, color='#06923E')
            ax3.plot(bulan_grp['bulan'], bulan_grp['prediksi'],
                     marker='o', color='#06923E', lw=2.2, markersize=7)
            ax3.set_title('Tren Rata-rata Prediksi per Bulan', fontsize=11,
                          fontweight='bold', color='#212121', pad=10,
                          fontfamily=FONT_BASE)
            ax3.set_xticks(bulan_grp['bulan'])
            ax3.set_xticklabels(bulan_grp['nama_bulan'], fontsize=8)
            ax3.yaxis.set_major_formatter(mticker.FuncFormatter(
                lambda x, _: f'{int(x):,}'))
            ax3.spines[['top','right']].set_visible(False)
            ax3.grid(color='#E0E0E0', linewidth=0.5)
            ax3.tick_params(axis='y', labelsize=8)
            for _, row in bulan_grp.iterrows():
                ax3.text(row['bulan'], row['prediksi'] + 40,
                         f"{int(row['prediksi']):,}", ha='center',
                         fontsize=7, color='#212121', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig3)
            img3 = fig_to_png(fig3)
            plt.close(fig3)
            st.download_button("Unduh Grafik 3",
                               data=img3, file_name="grafik_tren_bulanan.png",
                               mime="image/png", use_container_width=True)

        # ── Grafik 4: Perbandingan Prediksi antar Spot (Scatter / Boxplot) ──
        with g4:
            fig4, ax4 = plt.subplots(figsize=(6, 4.2))
            fig4.patch.set_facecolor('#F5F9F4')
            ax4.set_facecolor('#F5F9F4')

            order_spots = (df_hist.groupby('nama_spot')['prediksi']
                           .median().sort_values(ascending=False).index.tolist())
            data_box = [df_hist[df_hist['nama_spot']==s]['prediksi'].values
                        for s in order_spots]

            bp = ax4.boxplot(data_box, patch_artist=True, labels=order_spots,
                             medianprops=dict(color='#E67514', linewidth=2),
                             whiskerprops=dict(color='#555'),
                             capprops=dict(color='#555'),
                             flierprops=dict(marker='o', color='#888', markersize=4))
            for patch, color in zip(bp['boxes'], PALETTE[:len(order_spots)]):
                patch.set_facecolor(color)
                patch.set_alpha(0.65)

            ax4.set_title('Distribusi Prediksi per Spot', fontsize=11,
                          fontweight='bold', color='#212121', pad=10,
                          fontfamily=FONT_BASE)
            ax4.tick_params(axis='x', rotation=20, labelsize=8)
            ax4.tick_params(axis='y', labelsize=8)
            ax4.yaxis.set_major_formatter(mticker.FuncFormatter(
                lambda x, _: f'{int(x):,}'))
            ax4.spines[['top','right']].set_visible(False)
            ax4.grid(axis='y', color='#E0E0E0', linewidth=0.5)
            plt.tight_layout()
            st.pyplot(fig4)
            img4 = fig_to_png(fig4)
            plt.close(fig4)
            st.download_button("Unduh Grafik 4",
                               data=img4, file_name="grafik_distribusi_spot.png",
                               mime="image/png", use_container_width=True)

        # ── Grafik 5: Full width – Perbandingan total prediksi per spot per bulan ──
        if len(df_hist) > 0:
            st.markdown("---")
            st.markdown('<div class="section-title">Heatmap Prediksi: Spot × Bulan</div>',
                        unsafe_allow_html=True)
            pivot = df_hist.pivot_table(values='prediksi',
                                        index='nama_spot',
                                        columns='nama_bulan',
                                        aggfunc='mean').round(0)
            # Urutkan bulan
            bulan_order = [NAMA_BULAN[i] for i in range(1, 13) if NAMA_BULAN[i] in pivot.columns]
            pivot = pivot[[c for c in bulan_order if c in pivot.columns]]

            fig5, ax5 = plt.subplots(figsize=(12, 4.5))
            fig5.patch.set_facecolor('#F5F9F4')

            try:
                import seaborn as sns
                hm = sns.heatmap(pivot, annot=True, fmt='.0f', cmap='Greens',
                                 linewidths=0.4, linecolor='white',
                                 annot_kws={'size': 9}, ax=ax5,
                                 cbar_kws={'label': 'Rata-rata Prediksi', 'shrink': 0.85})
            except ImportError:
                im = ax5.imshow(pivot.values, cmap='Greens', aspect='auto')
                ax5.set_xticks(range(len(pivot.columns)))
                ax5.set_xticklabels(pivot.columns, rotation=45, ha='right')
                ax5.set_yticks(range(len(pivot.index)))
                ax5.set_yticklabels(pivot.index)
                plt.colorbar(im, ax=ax5, label='Rata-rata Prediksi')

            ax5.set_title('Heatmap Rata-rata Prediksi: Spot × Bulan',
                          fontsize=12, fontweight='bold', color='#212121',
                          pad=12, fontfamily=FONT_BASE)
            ax5.set_xlabel('Bulan', fontsize=10)
            ax5.set_ylabel('Spot Wisata', fontsize=10)
            ax5.tick_params(axis='both', labelsize=9)
            plt.tight_layout()
            st.pyplot(fig5)
            img5 = fig_to_png(fig5)
            plt.close(fig5)
            st.download_button("Unduh Heatmap",
                               data=img5, file_name="heatmap_prediksi.png",
                               mime="image/png", use_container_width=True)

    # ────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">Kelola Data</div>', unsafe_allow_html=True)
        st.warning("⚠️ Perhatian: Penghapusan data bersifat **permanen** dan tidak dapat dibatalkan.")

        col_del1, col_del2 = st.columns([1.5, 1])
        with col_del1:
            del_id = st.number_input(
                "Hapus data berdasarkan ID",
                min_value=1, step=1,
                help="Masukkan ID dari tabel riwayat untuk menghapus satu baris data"
            )
            if st.button("Hapus Data (ID terpilih)", type="secondary"):
                delete_prediction(int(del_id))
                st.success(f"Data dengan ID {int(del_id)} berhasil dihapus.")
                st.rerun()
        with col_del2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Hapus SEMUA Data", type="primary"):
                if 'confirm_clear' not in st.session_state:
                    st.session_state['confirm_clear'] = True
                    st.warning("Klik sekali lagi untuk konfirmasi penghapusan semua data.")
                else:
                    clear_all_predictions()
                    del st.session_state['confirm_clear']
                    st.success("Semua data prediksi telah dihapus.")
                    st.rerun()

        st.markdown("---")
        st.markdown("**Pratinjau Data yang Ada**")
        st.dataframe(
            df_hist[['id','tanggal','nama_spot','prediksi','catatan']].head(10),
            use_container_width=True,
            column_config={"prediksi": st.column_config.NumberColumn(format="%d 👤")}
        )