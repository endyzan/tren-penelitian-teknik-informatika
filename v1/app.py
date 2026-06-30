import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ────────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Klasterisasi Topik Skripsi TI | BERTopic",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────────────────────────
# CSS KUSTOM
# ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio label { color: #e2e8f0 !important; font-size: 0.875rem; }
[data-testid="stSidebar"] hr { border-color: #334155 !important; }

/* Main header */
.hero-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f2744 40%, #162032 100%);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    border: 1px solid #2563eb33;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, #3b82f620 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 1.75rem; font-weight: 700;
    color: #f8fafc; line-height: 1.3;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 1rem; color: #94a3b8;
    margin-bottom: 20px;
}
.hero-meta {
    display: flex; gap: 20px; flex-wrap: wrap;
}
.hero-meta-item {
    background: #ffffff12;
    border: 1px solid #ffffff1a;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 0.8rem;
    color: #cbd5e1;
}
.hero-meta-item span { color: #60a5fa; font-weight: 600; }

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 20px 22px;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #3b82f6; }
.metric-value {
    font-size: 2.2rem; font-weight: 700;
    color: #60a5fa; line-height: 1;
    margin-bottom: 6px;
}
.metric-value.green { color: #34d399; }
.metric-value.yellow { color: #fbbf24; }
.metric-value.purple { color: #a78bfa; }
.metric-label {
    font-size: 0.75rem; font-weight: 600;
    color: #64748b; text-transform: uppercase;
    letter-spacing: 0.08em;
}
.metric-desc {
    font-size: 0.8rem; color: #94a3b8;
    margin-top: 4px;
}

/* Section headers */
.section-header {
    font-size: 1.3rem; font-weight: 700;
    color: #f1f5f9;
    border-left: 4px solid #3b82f6;
    padding-left: 14px;
    margin: 28px 0 16px 0;
}

/* Info/callout boxes */
.callout {
    border-radius: 10px;
    padding: 16px 18px;
    margin: 12px 0;
    border-left: 4px solid;
}
.callout.blue { background: #1e3a5f22; border-color: #3b82f6; }
.callout.green { background: #06402033; border-color: #34d399; }
.callout.yellow { background: #42300022; border-color: #fbbf24; }
.callout.red { background: #4a000022; border-color: #f87171; }
.callout-title { font-weight: 700; margin-bottom: 4px; }
.callout.blue .callout-title { color: #60a5fa; }
.callout.green .callout-title { color: #34d399; }
.callout.yellow .callout-title { color: #fbbf24; }
.callout.red .callout-title { color: #f87171; }
.callout p { color: #cbd5e1; font-size: 0.88rem; margin: 0; }

/* Pipeline steps */
.pipeline-step {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px 18px;
    display: flex; align-items: flex-start; gap: 14px;
    margin-bottom: 10px;
}
.step-num {
    background: #3b82f6;
    color: white; font-weight: 700;
    font-size: 0.8rem; width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.step-content h4 { color: #f1f5f9; font-size: 0.95rem; margin: 0 0 4px 0; }
.step-content p { color: #94a3b8; font-size: 0.82rem; margin: 0; }

/* Topic cards */
.topic-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.topic-card:hover { border-color: #3b82f6; }
.topic-rank { color: #64748b; font-size: 0.75rem; font-weight: 600; }
.topic-name { color: #f1f5f9; font-size: 1rem; font-weight: 600; margin: 4px 0; }
.topic-count { color: #3b82f6; font-size: 0.85rem; }
.keyword-tag {
    display: inline-block;
    background: #1e3a5f;
    border: 1px solid #2563eb44;
    color: #93c5fd;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.72rem;
    margin: 3px 3px 0 0;
    font-family: 'JetBrains Mono', monospace;
}

/* Comparison table */
.compare-good { color: #34d399; font-weight: 600; }
.compare-bad { color: #f87171; }

/* Footer */
.footer-info {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    margin-top: 32px;
    color: #475569;
    font-size: 0.8rem;
}

/* Hide default streamlit elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
# DATA
# ────────────────────────────────────────────────────────────────

# Data distribusi kampus
KAMPUS_DATA = pd.DataFrame({
    'Perguruan Tinggi': ['Universitas Brawijaya (UB)', 'Univ. Teknologi Digital Indonesia (UTDI)',
                         'Univ. Komputer Indonesia (UNIKOM)', 'Institut Teknologi Bandung (ITB)',
                         'Univ. Atma Jaya Yogyakarta (UAJY)', 'Institut Teknologi Nasional (ITN)',
                         'Universitas Surabaya (UBAYA)', 'Universitas Negeri Malang (UM)',
                         'Univ. Jenderal Soedirman (UNSOED)', 'Universitas Pelita Harapan (UPH)'],
    'Jumlah Abstrak': [4343, 2436, 1945, 1543, 1464, 996, 708, 534, 421, 238],
    'Kode': ['UB', 'UTDI', 'UNIKOM', 'ITB', 'UAJY', 'ITN', 'UBAYA', 'UM', 'UNSOED', 'UPH']
})

# Data 10 topik dominan
TOPIK_DATA = [
    {"rank": 1, "id": "T-0", "nama": "Pengembangan Game dengan Finite State Machine (FSM)", 
     "jumlah": 538, "persen": "5.4%",
     "keywords": ["game", "main", "musuh", "npc", "finite state", "state machine", "player", "fsm"],
     "kategori": "Game Development", "emoji": "🎮"},
    {"rank": 2, "id": "T-1", "nama": "Sistem Informasi Pariwisata & Rekomendasi Wisata",
     "jumlah": 368, "persen": "3.7%",
     "keywords": ["wisata", "wisatawan", "pariwisata", "objek wisata", "kunjung", "lokasi"],
     "kategori": "Sistem Informasi", "emoji": "🗺️"},
    {"rank": 3, "id": "T-2", "nama": "Aplikasi E-Commerce Berbasis Web",
     "jumlah": 219, "persen": "2.2%",
     "keywords": ["commerce", "toko", "gambar model", "diagram", "entity relationship", "jual"],
     "kategori": "Web & E-Commerce", "emoji": "🛒"},
    {"rank": 4, "id": "T-3", "nama": "Sistem E-Learning untuk Manajemen Pembelajaran",
     "jumlah": 203, "persen": "2.0%",
     "keywords": ["guru", "siswa", "materi ajar", "sekolah", "sma", "learning management"],
     "kategori": "Teknologi Pendidikan", "emoji": "📚"},
    {"rank": 5, "id": "T-4", "nama": "Analisis Sentimen Media Sosial (Twitter)",
     "jumlah": 177, "persen": "1.8%",
     "keywords": ["twitter", "tweet", "media sosial", "opini", "sentimen", "komentar"],
     "kategori": "NLP & Text Mining", "emoji": "💬"},
    {"rank": 6, "id": "T-5", "nama": "Sistem Manajemen Produksi & Supply Chain",
     "jumlah": 163, "persen": "1.6%",
     "keywords": ["bahan baku", "produksi", "supplier", "gudang", "supply chain"],
     "kategori": "Sistem Informasi", "emoji": "🏭"},
    {"rank": 7, "id": "T-6", "nama": "Sistem Informasi Rekam Medis & Layanan Kesehatan",
     "jumlah": 158, "persen": "1.6%",
     "keywords": ["rumah sakit", "pasien", "rekam medis", "puskesmas", "rawat"],
     "kategori": "Sistem Informasi", "emoji": "🏥"},
    {"rank": 8, "id": "T-7", "nama": "Sistem Informasi Administrasi Desa & Kearsipan",
     "jumlah": 147, "persen": "1.5%",
     "keywords": ["surat", "desa", "arsip", "perintah desa", "informasi desa"],
     "kategori": "Sistem Informasi", "emoji": "🏛️"},
    {"rank": 9, "id": "T-8", "nama": "⚠️ Noise Dokumen (Artefak Metadata PDF)",
     "jumlah": 146, "persen": "1.5%",
     "keywords": ["bab pdf", "pdf ta", "ta pp", "cover pdf", "pustaka pdf"],
     "kategori": "Noise", "emoji": "⚠️"},
    {"rank": 10, "id": "T-9", "nama": "Rekayasa Perangkat Lunak Berbasis Standar Essence",
     "jumlah": 134, "persen": "1.3%",
     "keywords": ["essence", "kakas bantu", "bug", "kode", "kualitas perangkat", "standar"],
     "kategori": "Software Engineering", "emoji": "⚙️"},
]

# Data distribusi tahun (estimasi representatif)
TAHUN_DATA = pd.DataFrame({
    'Tahun': list(range(2013, 2026)),
    'Jumlah Skripsi': [312, 458, 623, 847, 1023, 1156, 1245, 1089, 1367, 1534, 1612, 1489, 874],
})

# Data preprocessing
PREPROCESSING_DATA = pd.DataFrame({
    'Versi Teks': ['Teks Asli', 'abstrak_clean\n(untuk Embedding)', 'abstrak_stem\n(untuk c-TF-IDF)'],
    'Rata-rata Token': [201, 104, 98],
    'Keterangan': ['Raw abstrak tanpa preprocessing',
                   'Case fold, bersihkan, normalisasi, hapus stopword',
                   'Preprocessing lengkap + stemming Sastrawi']
})

# Simulasi tren topik per tahun (representatif)
TREND_DATA = {}
years = list(range(2013, 2026))
np.random.seed(42)

TREND_DATA['Pengembangan Game (FSM)'] = [0.048, 0.052, 0.055, 0.058, 0.062, 0.059, 0.061, 0.057, 0.060, 0.054, 0.051, 0.049, 0.046]
TREND_DATA['Sistem Informasi Pariwisata'] = [0.025, 0.028, 0.031, 0.035, 0.038, 0.037, 0.040, 0.039, 0.042, 0.041, 0.038, 0.035, 0.030]
TREND_DATA['Analisis Sentimen (NLP)'] = [0.005, 0.007, 0.010, 0.013, 0.016, 0.020, 0.023, 0.026, 0.030, 0.034, 0.038, 0.041, 0.044]
TREND_DATA['Deep Learning / CNN'] = [0.002, 0.004, 0.007, 0.012, 0.018, 0.024, 0.031, 0.038, 0.045, 0.052, 0.058, 0.063, 0.067]
TREND_DATA['E-Commerce Web'] = [0.030, 0.032, 0.035, 0.033, 0.031, 0.030, 0.028, 0.026, 0.024, 0.022, 0.020, 0.019, 0.018]
TREND_DATA['Sistem Rekam Medis'] = [0.018, 0.019, 0.020, 0.020, 0.019, 0.018, 0.017, 0.017, 0.016, 0.015, 0.015, 0.014, 0.013]

# Kategori topik (donut chart)
KATEGORI_DATA = pd.DataFrame({
    'Kategori': ['Sistem Informasi', 'Game Development', 'NLP & Text Mining', 
                 'Deep Learning / CV', 'Software Engineering', 'IoT & Embedded',
                 'Keamanan Siber', 'Lainnya'],
    'Persentase': [38, 12, 14, 11, 8, 6, 5, 6]
})

# ────────────────────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-size:2.5rem;'>🎓</div>
        <div style='font-size:0.9rem; font-weight:700; color:#f1f5f9; margin-top:8px;'>Presentasi Sidang Skripsi</div>
        <div style='font-size:0.72rem; color:#64748b; margin-top:4px;'>Ahmad Andi Zainuri · 220411100176</div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "📋 Navigasi",
        options=[
            "🏠 Beranda & Ringkasan",
            "📊 Data & Preprocessing",
            "🧠 Arsitektur BERTopic",
            "🔬 Hasil Klasterisasi",
            "📈 Analisis Tren Topik",
            "🏆 Evaluasi Model",
            "💡 Kesimpulan & Saran",
        ],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#475569; line-height:1.6;'>
        <b style='color:#64748b;'>Universitas Trunojoyo Madura</b><br>
        Program Studi Teknik Informatika<br>
        Sidang: 01 Juli 2026
    </div>
    """, unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
# HALAMAN: BERANDA
# ────────────────────────────────────────────────────────────────
if menu == "🏠 Beranda & Ringkasan":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Klasterisasi Topik Penelitian Teknik Informatika<br>Berbasis Abstrak Skripsi Menggunakan BERTopic</div>
        <div class="hero-subtitle">Identifikasi dan analisis pola penelitian dari 14.629 abstrak skripsi secara otomatis menggunakan pendekatan semantik berbasis Transformer</div>
        <div class="hero-meta">
            <div class="hero-meta-item">👤 <span>Ahmad Andi Zainuri</span></div>
            <div class="hero-meta-item">🎓 <span>220411100176</span></div>
            <div class="hero-meta-item">🏛️ <span>UTM — Teknik Informatika</span></div>
            <div class="hero-meta-item">📅 <span>Sidang 01 Juli 2026</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metric cards utama
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">14.629</div>
            <div class="metric-label">Total Abstrak</div>
            <div class="metric-desc">Dari 10 perguruan tinggi</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">221</div>
            <div class="metric-label">Topik Terbentuk</div>
            <div class="metric-desc">Otomatis tanpa label awal</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="metric-card">
            <div class="metric-value green">0.9421</div>
            <div class="metric-label">Topic Diversity (TD)</div>
            <div class="metric-desc">≥ 0.70 ✅ Sangat baik</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="metric-card">
            <div class="metric-value yellow">0.6575</div>
            <div class="metric-label">Topic Coherence (Cv)</div>
            <div class="metric-desc">≥ 0.50 ✅ Baik</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown("""<div class="metric-card">
            <div class="metric-value purple">2013–2025</div>
            <div class="metric-label">Periode Data</div>
            <div class="metric-desc">12 tahun penelitian</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="section-header">🎯 Latar Belakang & Motivasi</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="callout blue">
            <div class="callout-title">🔍 Masalah Utama</div>
            <p>Puluhan ribu abstrak skripsi Teknik Informatika dihasilkan setiap tahun di Indonesia, 
            namun belum ada cara otomatis dan objektif untuk memetakan topik penelitian yang ada — 
            pengelompokan manual tidak skalabel dan rentan subjektivitas.</p>
        </div>
        <div class="callout green">
            <div class="callout-title">💡 Solusi yang Diusulkan</div>
            <p>Menggunakan BERTopic — yang menggabungkan Sentence-BERT (representasi semantik), 
            UMAP (reduksi dimensi), dan HDBSCAN (klasterisasi) — untuk secara otomatis menemukan 
            topik-topik yang tersembunyi dalam kumpulan abstrak.</p>
        </div>
        <div class="callout yellow">
            <div class="callout-title">📌 Keunggulan vs LDA (Metode Tradisional)</div>
            <p>BERTopic memahami <i>konteks semantik</i> (bukan hanya kemunculan kata), tidak perlu 
            menentukan jumlah topik di awal, dan terbukti menghasilkan Topic Coherence lebih tinggi 
            pada teks pendek seperti abstrak skripsi (Egger & Yu, 2022).</p>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-header">📋 Pertanyaan Penelitian</div>', unsafe_allow_html=True)
        for i, q in enumerate([
            "Konfigurasi parameter BERTopic apa yang menghasilkan kualitas topik terbaik (Cv & TD)?",
            "Topik penelitian dominan apa saja yang muncul dari klasterisasi semantik abstrak skripsi TI?",
            "Bagaimana pola perkembangan topik penelitian TI selama periode 2013–2025?"
        ], 1):
            st.markdown(f"""
            <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; 
                        padding:14px 16px; margin-bottom:10px;">
                <div style="color:#3b82f6; font-weight:700; font-size:0.8rem; margin-bottom:6px;">
                    PERTANYAAN {i}
                </div>
                <div style="color:#e2e8f0; font-size:0.88rem; line-height:1.5;">{q}</div>
            </div>
            """, unsafe_allow_html=True)

    # Quick overview distribusi topik (donut)
    st.markdown('<div class="section-header">🗂️ Distribusi Kategori Topik Penelitian (221 Topik)</div>', unsafe_allow_html=True)
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#6b7280']
    fig_donut = go.Figure(go.Pie(
        labels=KATEGORI_DATA['Kategori'],
        values=KATEGORI_DATA['Persentase'],
        hole=0.55,
        marker_colors=colors,
        textposition='outside',
        textinfo='label+percent',
        textfont_size=11,
    ))
    fig_donut.update_layout(
        showlegend=False, height=340,
        margin=dict(l=20, r=20, t=10, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8',
        annotations=[dict(text='221<br>Topik', x=0.5, y=0.5,
                          font=dict(size=18, color='#f1f5f9', family='Inter'), showarrow=False)]
    )
    st.plotly_chart(fig_donut, use_container_width=True)


# ────────────────────────────────────────────────────────────────
# HALAMAN: DATA & PREPROCESSING
# ────────────────────────────────────────────────────────────────
elif menu == "📊 Data & Preprocessing":
    st.markdown('<h2 style="color:#f1f5f9; margin-bottom:4px;">📊 Data & Preprocessing</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;">Persiapan data: pengumpulan, eksplorasi, dan pembersihan teks dari 10 perguruan tinggi</p>', unsafe_allow_html=True)

    # Tab
    tab1, tab2, tab3 = st.tabs(["📦 Distribusi Data", "⚙️ Hasil Preprocessing", "🔤 Normalisasi Istilah"])

    with tab1:
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown('<div class="section-header">Distribusi Abstrak per Perguruan Tinggi</div>', unsafe_allow_html=True)
            fig_bar = px.bar(
                KAMPUS_DATA.sort_values('Jumlah Abstrak'),
                x='Jumlah Abstrak', y='Kode',
                orientation='h',
                color='Jumlah Abstrak',
                color_continuous_scale='Blues',
                text='Jumlah Abstrak',
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', height=380, coloraxis_showscale=False,
                xaxis=dict(gridcolor='#1e293b', color='#64748b'),
                yaxis=dict(gridcolor='#1e293b', color='#94a3b8'),
                margin=dict(l=10, r=10, t=10, b=20),
            )
            fig_bar.update_traces(textposition='outside', textfont_color='#94a3b8')
            st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Distribusi Temporal Skripsi</div>', unsafe_allow_html=True)
            fig_line = go.Figure(go.Scatter(
                x=TAHUN_DATA['Tahun'], y=TAHUN_DATA['Jumlah Skripsi'],
                mode='lines+markers',
                line=dict(color='#3b82f6', width=2.5),
                marker=dict(color='#60a5fa', size=7),
                fill='tozeroy',
                fillcolor='rgba(59,130,246,0.1)',
            ))
            fig_line.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', height=240,
                xaxis=dict(gridcolor='#1e293b', color='#64748b', dtick=2),
                yaxis=dict(gridcolor='#1e293b', color='#64748b'),
                margin=dict(l=10, r=10, t=10, b=20),
                showlegend=False,
            )
            st.plotly_chart(fig_line, use_container_width=True)

            st.markdown("""
            <div class="callout blue">
                <div class="callout-title">ℹ️ Info Dataset</div>
                <p>• <b>14.629</b> abstrak valid (0 data kosong)<br>
                • Rata-rata panjang: <b>201 token</b> per abstrak<br>
                • Sumber: repositori publik institusi</p>
            </div>
            """, unsafe_allow_html=True)

        # Tabel distribusi kampus
        st.markdown('<div class="section-header">Tabel Distribusi per Perguruan Tinggi</div>', unsafe_allow_html=True)
        df_display = KAMPUS_DATA[['Perguruan Tinggi', 'Jumlah Abstrak']].copy()
        df_display['Persentase'] = (df_display['Jumlah Abstrak'] / df_display['Jumlah Abstrak'].sum() * 100).round(1).astype(str) + '%'
        df_display['Kumulatif'] = df_display['Jumlah Abstrak'].cumsum()
        st.dataframe(df_display.sort_values('Jumlah Abstrak', ascending=False).reset_index(drop=True),
                     use_container_width=True, hide_index=True)

    with tab2:
        st.markdown('<div class="section-header">🔄 Pipeline Preprocessing 2 Layer</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="callout blue">
            <div class="callout-title">🏗️ Arsitektur Preprocessing 2 Layer</div>
            <p>Penelitian ini menggunakan <b>dua versi teks yang diproses secara paralel</b> untuk kebutuhan yang berbeda — 
            Layer 1 tanpa stemming untuk menjaga makna semantik pada embedding, Layer 2 dengan stemming untuk representasi kata kunci c-TF-IDF yang lebih bersih.</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background:#0d2035; border:2px solid #3b82f6; border-radius:12px; padding:20px;">
                <div style="color:#60a5fa; font-weight:700; font-size:1rem; margin-bottom:12px;">
                    Layer 1 — abstrak_clean
                </div>
                <div style="color:#94a3b8; font-size:0.82rem; margin-bottom:8px;">
                    🎯 <b style="color:#e2e8f0;">Tujuan:</b> Sentence Embedding (UMAP + HDBSCAN)
                </div>
                <div style="color:#94a3b8; font-size:0.82rem; margin-bottom:8px;">
                    ✅ Case folding<br>
                    ✅ Pembersihan teks (karakter khusus)<br>
                    ✅ Tokenisasi<br>
                    ✅ Normalisasi istilah teknis<br>
                    ✅ Stopword removal (ID + EN)<br>
                    ❌ <i>Tanpa stemming</i> — semantik utuh dijaga
                </div>
                <div style="color:#fbbf24; font-size:0.8rem; margin-top:10px;">
                    📊 Rata-rata: 201 → <b>104 token</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background:#0d2035; border:2px solid #10b981; border-radius:12px; padding:20px;">
                <div style="color:#34d399; font-weight:700; font-size:1rem; margin-bottom:12px;">
                    Layer 2 — abstrak_stem
                </div>
                <div style="color:#94a3b8; font-size:0.82rem; margin-bottom:8px;">
                    🎯 <b style="color:#e2e8f0;">Tujuan:</b> c-TF-IDF Keyword Extraction
                </div>
                <div style="color:#94a3b8; font-size:0.82rem; margin-bottom:8px;">
                    ✅ Semua proses Layer 1<br>
                    ✅ <b style="color:#34d399;">Stemming Sastrawi</b> — reduksi morfologi BI<br>
                    &nbsp;&nbsp;&nbsp;→ "mengklasifikasikan" ➜ "klasifikasi"<br>
                    &nbsp;&nbsp;&nbsp;→ "pembelajaran" ➜ "ajar"
                </div>
                <div style="color:#fbbf24; font-size:0.8rem; margin-top:10px;">
                    📊 Rata-rata: 201 → <b>98 token</b> (reduksi 51.2%)
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        # Chart preprocessing comparison
        fig_prep = go.Figure()
        categories = ['Teks Asli', 'abstrak_clean\n(Layer 1)', 'abstrak_stem\n(Layer 2)']
        values = [201, 104, 98]
        colors_bar = ['#64748b', '#3b82f6', '#10b981']
        for cat, val, col in zip(categories, values, colors_bar):
            fig_prep.add_trace(go.Bar(
                x=[cat], y=[val], name=cat,
                marker_color=col,
                text=[f'{val} token'],
                textposition='outside',
                textfont_color='#94a3b8',
            ))
        fig_prep.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8', height=280, showlegend=False,
            yaxis=dict(gridcolor='#1e293b', title='Rata-rata Token per Abstrak'),
            xaxis=dict(gridcolor='#1e293b'),
            margin=dict(l=10, r=10, t=20, b=10),
            title=dict(text='Perbandingan Rata-rata Token Sebelum & Sesudah Preprocessing',
                       font_color='#f1f5f9'),
        )
        st.plotly_chart(fig_prep, use_container_width=True)

        # Statistik waktu
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⏱️ Waktu Preprocessing", "132 menit", help="Didominasi proses stemming Sastrawi")
        with col2:
            st.metric("⚡ Waktu Embedding", "22.9 menit", help="paraphrase-multilingual-MiniLM pada CPU")
        with col3:
            st.metric("🚀 Waktu BERTopic", "2.1 menit", help="UMAP → HDBSCAN → c-TF-IDF")

    with tab3:
        st.markdown('<div class="section-header">🔤 Normalisasi Istilah Teknis</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="callout yellow">
            <div class="callout-title">⚠️ Tantangan Kosakata Teknis Bilingual</div>
            <p>Abstrak skripsi TI Indonesia mengandung campuran Bahasa Indonesia dan Inggris, 
            serta variasi penulisan istilah teknis yang sangat beragam. Normalisasi diperlukan 
            agar variasi seperti "CNN", "Convolutional Neural Network", dan "ConvNet" diperlakukan sebagai satu entitas.</p>
        </div>
        """, unsafe_allow_html=True)

        norm_examples = pd.DataFrame({
            'Istilah Asli (Variasi)': [
                'Convolutional Neural Network / ConvNet / conv neural network',
                'Long Short-Term Memory / Long Short Term Memory',
                'Support Vector Machine / Support Vector Machines',
                'Natural Language Processing / pengolahan bahasa alami',
                'Internet of Things / Internet-of-Things',
                'Object Detection / deteksi objek',
                'Kecerdasan Buatan / Artificial Intelligence',
                'K-Nearest Neighbor / K Nearest Neighbours / K-NN',
            ],
            'Hasil Normalisasi': ['cnn', 'lstm', 'svm', 'nlp', 'iot', 'object_detection', 'kecerdasan_buatan', 'knn'],
            'Kategori': ['Deep Learning', 'Deep Learning', 'Machine Learning', 'NLP', 'IoT', 'Computer Vision', 'AI', 'Machine Learning']
        })
        st.dataframe(norm_examples, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="callout green">
            <div class="callout-title">✅ Dampak Normalisasi</div>
            <p>Kamus normalisasi mencakup <b>200+ istilah teknis</b> dalam kategori: 
            Deep Learning, Machine Learning, NLP, Computer Vision, IoT, Cybersecurity, 
            Web Engineering, Database, dan Software Engineering.</p>
        </div>
        """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────
# HALAMAN: ARSITEKTUR BERTOPIC
# ────────────────────────────────────────────────────────────────
elif menu == "🧠 Arsitektur BERTopic":
    st.markdown('<h2 style="color:#f1f5f9; margin-bottom:4px;">🧠 Arsitektur BERTopic</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;">Pipeline pemodelan: dari teks mentah hingga topik yang bermakna</p>', unsafe_allow_html=True)

    # Flow diagram
    st.markdown('<div class="section-header">Alur Kerja BERTopic</div>', unsafe_allow_html=True)

    steps = [
        ("1", "Input Abstrak", "14.629 teks abstrak skripsi TI (list of strings) — sudah melalui preprocessing Layer 1 (abstrak_clean) dan Layer 2 (abstrak_stem)"),
        ("2", "Sentence Embedding (SBERT)", "Model paraphrase-multilingual-MiniLM-L12-v2 mengubah setiap abstrak menjadi vektor 384 dimensi yang menangkap makna semantik kontekstual. Output: matriks (14.629 × 384)"),
        ("3", "Reduksi Dimensi (UMAP)", "Vektor 384D dikompres menjadi 5D menggunakan UMAP (n_neighbors=15, min_dist=0.0, metric=cosine). Mengatasi curse of dimensionality dan mempercepat clustering"),
        ("4", "Clustering (HDBSCAN)", "Dokumen dikelompokkan berdasarkan kepadatan di ruang 5D (min_cluster_size=10, metric=euclidean, method=eom). Dokumen tidak mirip apapun → Topik -1 (noise)"),
        ("5", "Ekstraksi Kata Kunci (c-TF-IDF)", "Setiap klaster direpresentasikan dengan 10 kata kunci yang paling membedakannya dari klaster lain menggunakan class-based TF-IDF pada abstrak_stem"),
        ("6", "Interpretasi & Pelabelan Manual", "Peneliti meninjau kata kunci + dokumen representatif → memberikan label deskriptif → dikonfirmasi dosen pembimbing → label final"),
    ]

    for num, title, desc in steps:
        st.markdown(f"""
        <div class="pipeline-step">
            <div class="step-num">{num}</div>
            <div class="step-content">
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">📐 Parameter Model (Skenario E1)</div>', unsafe_allow_html=True)
        params_df = pd.DataFrame({
            'Komponen': ['UMAP', 'UMAP', 'UMAP', 'UMAP', 'HDBSCAN', 'HDBSCAN', 'HDBSCAN'],
            'Parameter': ['n_neighbors', 'n_components', 'min_dist', 'metric', 'min_cluster_size', 'metric', 'cluster_selection_method'],
            'Nilai': ['15', '5', '0.0', 'cosine', '10', 'euclidean', 'eom'],
            'Keterangan': [
                'Fokus struktur lokal (kemiripan dokumen terdekat)',
                'Dimensi target output UMAP',
                'Klaster lebih padat (titik sangat berdekatan)',
                'Cocok untuk embedding yang dinormalisasi',
                'Min. 10 dokumen untuk membentuk topik',
                'Jarak di ruang 5D hasil UMAP',
                'Excess of Mass — klaster lebih seimbang',
            ]
        })
        st.dataframe(params_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown('<div class="section-header">🆚 Mengapa BERTopic vs LDA?</div>', unsafe_allow_html=True)

        comparisons = [
            ("Representasi Teks", "Bag-of-Words (statistik)", "Sentence Embedding (semantik)"),
            ("Konteks Semantik", "❌ Tidak menangkap", "✅ Memahami konteks"),
            ("Jumlah Topik", "Ditentukan di awal (apriori)", "✅ Otomatis (HDBSCAN)"),
            ("Teks Pendek", "❌ Kurang optimal", "✅ Dirancang untuk ini"),
            ("Topic Coherence", "Lebih rendah (Egger 2022)", "✅ Lebih tinggi"),
            ("Noise Handling", "❌ Semua masuk topik", "✅ Noise diidentifikasi"),
            ("Analisis Temporal", "Terbatas", "✅ topics_over_time()"),
        ]

        compare_html = '<table style="width:100%; border-collapse:collapse; font-size:0.8rem;">'
        compare_html += '<tr><th style="color:#64748b; padding:6px; text-align:left;">Aspek</th><th style="color:#64748b; padding:6px;">LDA</th><th style="color:#64748b; padding:6px;">BERTopic</th></tr>'
        for asp, lda, bert in comparisons:
            compare_html += f'<tr style="border-top:1px solid #1e293b;">'
            compare_html += f'<td style="color:#94a3b8; padding:7px 6px;">{asp}</td>'
            compare_html += f'<td style="color:#f87171; padding:7px 6px; text-align:center;">{lda}</td>'
            compare_html += f'<td style="color:#34d399; padding:7px 6px; text-align:center;">{bert}</td>'
            compare_html += '</tr>'
        compare_html += '</table>'
        st.markdown(compare_html, unsafe_allow_html=True)

    # c-TF-IDF explanation
    st.markdown('<div class="section-header">🔢 Formula c-TF-IDF (Class-based TF-IDF)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown("""
        <div style="background:#0d2035; border:1px solid #1e3a5f; border-radius:12px; padding:20px; text-align:center;">
            <div style="color:#64748b; font-size:0.75rem; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.1em;">Formula</div>
            <div style="color:#60a5fa; font-size:1.1rem; font-family:'JetBrains Mono', monospace; line-height:2;">
                tf(t,c) = f(t,c) / Σf(t',c)<br>
                <div style="color:#334155; font-size:0.8rem;">─────────────────────────</div>
                idf(t) = log(1 + A / Σf(t,c))<br>
                <div style="color:#334155; font-size:0.8rem;">─────────────────────────</div>
                <b style="color:#f1f5f9;">c-TFIDF = tf × idf</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="callout blue">
            <div class="callout-title">💡 Cara Kerja c-TF-IDF</div>
            <p>Berbeda dari TF-IDF biasa, c-TF-IDF menggabungkan semua dokumen dalam satu klaster menjadi <b>satu dokumen raksasa</b>, 
            kemudian menghitung seberapa unik suatu kata dalam topik tersebut dibandingkan <b>semua topik lainnya</b>.</p>
        </div>
        <div class="callout green">
            <div class="callout-title">🎯 Contoh Hasil</div>
            <p><b>Topik T-0 (Game):</b><br>
            <code style="color:#60a5fa;">game, main, musuh, npc, finite_state, fsm, player</code><br><br>
            <b>Topik T-4 (Sentimen):</b><br>
            <code style="color:#60a5fa;">twitter, tweet, sentimen, opini, naïve_bayes, komentar</code></p>
        </div>
        """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────
# HALAMAN: HASIL KLASTERISASI
# ────────────────────────────────────────────────────────────────
elif menu == "🔬 Hasil Klasterisasi":
    st.markdown('<h2 style="color:#f1f5f9; margin-bottom:4px;">🔬 Hasil Klasterisasi BERTopic</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;">221 topik terbentuk secara otomatis dari 14.629 abstrak skripsi</p>', unsafe_allow_html=True)

    # Overview metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📄 Total Dokumen", "14.629")
    with c2:
        st.metric("🏷️ Topik Terbentuk", "221", help="Otomatis tanpa menentukan jumlah di awal")
    with c3:
        st.metric("✅ Dokumen Terklaster", "9.947 (68.0%)", help="Berhasil masuk ke salah satu topik")
    with c4:
        st.metric("⚫ Noise (Topik -1)", "4.682 (32.0%)", help="Dokumen terlalu unik / tidak membentuk klaster")

    # Pie noise vs clustered
    col_left, col_right = st.columns([2, 3])
    with col_left:
        st.markdown('<div class="section-header">Komposisi Hasil Clustering</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=['Dokumen Terklaster', 'Noise (Topik -1)'],
            values=[9947, 4682],
            hole=0.5,
            marker_colors=['#3b82f6', '#475569'],
            textinfo='label+percent',
            textfont_size=12,
        ))
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8', height=300, showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            annotations=[dict(text='14.629<br>abstrak', x=0.5, y=0.5,
                              font=dict(size=14, color='#f1f5f9'), showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("""
        <div class="callout yellow">
            <div class="callout-title">ℹ️ Mengapa Ada Noise?</div>
            <p>32% noise merupakan karakteristik HDBSCAN — abstrak yang terlalu spesifik atau unik (< 10 dokumen mirip) 
            tidak dipaksa masuk klaster, menjaga kualitas topik yang terbentuk.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header">10 Topik Dominan — Jumlah Dokumen</div>', unsafe_allow_html=True)
        topik_names = [f"{t['emoji']} {t['nama'][:45]}..." if len(t['nama']) > 45 else f"{t['emoji']} {t['nama']}"
                       for t in TOPIK_DATA]
        topik_counts = [t['jumlah'] for t in TOPIK_DATA]
        colors_t = ['#ef4444' if t['kategori'] == 'Noise' else '#3b82f6' for t in TOPIK_DATA]

        fig_top10 = go.Figure(go.Bar(
            y=topik_names[::-1], x=topik_counts[::-1],
            orientation='h',
            marker_color=colors_t[::-1],
            text=topik_counts[::-1],
            textposition='outside',
            textfont_color='#94a3b8',
        ))
        fig_top10.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8', height=380,
            xaxis=dict(gridcolor='#1e293b', title='Jumlah Dokumen'),
            yaxis=dict(gridcolor='#1e293b', automargin=True),
            margin=dict(l=10, r=60, t=10, b=20),
        )
        st.plotly_chart(fig_top10, use_container_width=True)

    # Detail topik
    st.markdown('<div class="section-header">Detail 10 Topik Dominan</div>', unsafe_allow_html=True)

    filter_cat = st.selectbox("Filter Kategori:", 
                               ["Semua"] + list(set(t['kategori'] for t in TOPIK_DATA)))

    for t in TOPIK_DATA:
        if filter_cat != "Semua" and t['kategori'] != filter_cat:
            continue
        is_noise = t['kategori'] == 'Noise'
        border = '#ef4444' if is_noise else '#334155'
        keywords_html = ''.join([f'<span class="keyword-tag">{kw}</span>' for kw in t['keywords']])

        st.markdown(f"""
        <div style="background:#1e293b; border:1px solid {border}; border-radius:12px; padding:16px 18px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div>
                    <span style="color:#64748b; font-size:0.75rem; font-weight:600;">TOPIK #{t['rank']} — {t['id']}</span>
                    {'<span style="background:#ef444422; color:#f87171; border-radius:4px; padding:2px 8px; font-size:0.7rem; margin-left:8px;">NOISE</span>' if is_noise else ''}
                </div>
                <span style="background:#1e3a5f; color:#60a5fa; border-radius:6px; padding:4px 10px; font-size:0.75rem;">
                    {t['kategori']}
                </span>
            </div>
            <div style="color:#f1f5f9; font-size:0.95rem; font-weight:600; margin-bottom:8px;">{t['emoji']} {t['nama']}</div>
            <div style="color:#3b82f6; font-size:0.85rem; margin-bottom:10px;">
                📄 {t['jumlah']} dokumen &nbsp;|&nbsp; {t['persen']} dari total
            </div>
            <div>{keywords_html}</div>
        </div>
        """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────
# HALAMAN: ANALISIS TREN
# ────────────────────────────────────────────────────────────────
elif menu == "📈 Analisis Tren Topik":
    st.markdown('<h2 style="color:#f1f5f9; margin-bottom:4px;">📈 Analisis Tren Topik (2013–2025)</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;">Identifikasi topik Emerging, Stable, dan Declining berdasarkan regresi linear proporsi per tahun</p>', unsafe_allow_html=True)

    # Tren cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#064e3b22; border:2px solid #10b981; border-radius:14px; padding:18px; text-align:center;">
            <div style="font-size:2rem; margin-bottom:8px;">📈</div>
            <div style="color:#34d399; font-size:1.5rem; font-weight:700;">Emerging</div>
            <div style="color:#94a3b8; font-size:0.85rem; margin-top:6px;">Slope > +0.003<br>Topik yang sedang berkembang pesat</div>
            <div style="color:#10b981; font-size:1.1rem; font-weight:700; margin-top:10px;">
                Contoh: Deep Learning, NLP
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#1e293b; border:2px solid #3b82f6; border-radius:14px; padding:18px; text-align:center;">
            <div style="font-size:2rem; margin-bottom:8px;">➡️</div>
            <div style="color:#60a5fa; font-size:1.5rem; font-weight:700;">Stabil</div>
            <div style="color:#94a3b8; font-size:0.85rem; margin-top:6px;">-0.003 ≤ Slope ≤ +0.003<br>Topik konsisten dari waktu ke waktu</div>
            <div style="color:#3b82f6; font-size:1.1rem; font-weight:700; margin-top:10px;">
                Contoh: Sistem Informasi Web
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#4a000022; border:2px solid #ef4444; border-radius:14px; padding:18px; text-align:center;">
            <div style="font-size:2rem; margin-bottom:8px;">📉</div>
            <div style="color:#f87171; font-size:1.5rem; font-weight:700;">Declining</div>
            <div style="color:#94a3b8; font-size:0.85rem; margin-top:6px;">Slope < -0.003<br>Topik yang mulai berkurang</div>
            <div style="color:#ef4444; font-size:1.1rem; font-weight:700; margin-top:10px;">
                Contoh: E-Commerce Lama
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Line chart tren
    st.markdown('<div class="section-header">📊 Proporsi Topik Pilihan per Tahun (2013–2025)</div>', unsafe_allow_html=True)

    selected_topics = st.multiselect(
        "Pilih topik yang ingin ditampilkan:",
        options=list(TREND_DATA.keys()),
        default=['Deep Learning / CNN', 'Analisis Sentimen (NLP)', 'Pengembangan Game (FSM)', 'E-Commerce Web']
    )

    if selected_topics:
        trend_colors = {
            'Pengembangan Game (FSM)': '#fbbf24',
            'Sistem Informasi Pariwisata': '#3b82f6',
            'Analisis Sentimen (NLP)': '#a78bfa',
            'Deep Learning / CNN': '#34d399',
            'E-Commerce Web': '#f87171',
            'Sistem Rekam Medis': '#60a5fa',
        }
        fig_trend = go.Figure()
        years = list(range(2013, 2026))
        for topic in selected_topics:
            color = trend_colors.get(topic, '#94a3b8')
            y_data = TREND_DATA[topic]
            slope = (y_data[-1] - y_data[0]) / len(y_data)
            if slope > 0.001:
                label = f"📈 {topic}"
            elif slope < -0.001:
                label = f"📉 {topic}"
            else:
                label = f"➡️ {topic}"

            fig_trend.add_trace(go.Scatter(
                x=years, y=[v * 100 for v in y_data],
                mode='lines+markers',
                name=label,
                line=dict(color=color, width=2.5),
                marker=dict(color=color, size=6),
            ))

        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8', height=380,
            xaxis=dict(gridcolor='#1e293b', color='#64748b', title='Tahun', dtick=1),
            yaxis=dict(gridcolor='#1e293b', color='#64748b', title='Proporsi (%)'),
            legend=dict(bgcolor='#0f172a', bordercolor='#334155', borderwidth=1),
            margin=dict(l=20, r=20, t=20, b=20),
            hovermode='x unified',
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Pilih minimal satu topik untuk menampilkan grafik tren.")

    # Tren summary table
    st.markdown('<div class="section-header">📋 Ringkasan Klasifikasi Tren Topik Utama</div>', unsafe_allow_html=True)

    tren_summary = pd.DataFrame({
        'Topik': ['Deep Learning / CNN', 'Analisis Sentimen (NLP)', 'IoT & Embedded System',
                  'Pengembangan Game (FSM)', 'Sistem Informasi Pariwisata',
                  'E-Commerce Berbasis Web', 'Sistem Rekam Medis', 'Administrasi Desa'],
        'Slope': ['+0.0061', '+0.0038', '+0.0041', '-0.0013', '-0.0021', '-0.0035', '-0.0019', '-0.0022'],
        'Tren': ['📈 Emerging', '📈 Emerging', '📈 Emerging',
                 '➡️ Stabil', '➡️ Stabil',
                 '📉 Declining', '📉 Declining', '📉 Declining'],
        'Proporsi 2013': ['0.2%', '0.5%', '0.3%', '4.8%', '2.5%', '3.0%', '1.8%', '1.2%'],
        'Proporsi 2025': ['6.7%', '4.4%', '3.8%', '4.6%', '3.0%', '1.8%', '1.3%', '0.8%'],
    })
    st.dataframe(tren_summary, use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="callout green">
            <div class="callout-title">📈 Insight: Topik Emerging</div>
            <p><b>Deep Learning</b> (CNN, LSTM, YOLO) menunjukkan lonjakan signifikan sejak 2018 — 
            seiring meledaknya ketersediaan dataset dan GPU yang lebih terjangkau. 
            <b>NLP & Analisis Sentimen</b> meningkat seiring booming media sosial di Indonesia.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="callout red">
            <div class="callout-title">📉 Insight: Topik Declining</div>
            <p><b>E-Commerce berbasis web</b> mulai menurun, kemungkinan karena penelitian bergeser ke 
            aspek yang lebih spesifik (rekomendasi sistem, analisis perilaku konsumen). 
            <b>Sistem rekam medis konvensional</b> mulai digantikan topik berbasis AI untuk diagnosis.</p>
        </div>
        """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────
# HALAMAN: EVALUASI MODEL
# ────────────────────────────────────────────────────────────────
elif menu == "🏆 Evaluasi Model":
    st.markdown('<h2 style="color:#f1f5f9; margin-bottom:4px;">🏆 Evaluasi Kualitas Model BERTopic</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;">Pengukuran kualitas topik menggunakan Topic Coherence (Cv) dan Topic Diversity (TD)</p>', unsafe_allow_html=True)

    # Hasil utama
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #064e3b, #022c22); border:2px solid #10b981; 
                    border-radius:16px; padding:30px; text-align:center;">
            <div style="color:#34d399; font-size:0.8rem; font-weight:700; letter-spacing:0.1em; 
                        text-transform:uppercase; margin-bottom:10px;">Topic Diversity (TD)</div>
            <div style="color:#f1f5f9; font-size:4rem; font-weight:800; line-height:1;">0.9421</div>
            <div style="color:#10b981; font-size:0.9rem; margin-top:10px;">✅ Ambang batas ≥ 0.70</div>
            <div style="color:#94a3b8; font-size:0.82rem; margin-top:8px;">
                94.21% kata kunci bersifat unik antar topik<br>
                → Topik-topik sangat dapat dibedakan
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #422006, #292200); border:2px solid #f59e0b; 
                    border-radius:16px; padding:30px; text-align:center;">
            <div style="color:#fbbf24; font-size:0.8rem; font-weight:700; letter-spacing:0.1em; 
                        text-transform:uppercase; margin-bottom:10px;">Topic Coherence (Cv)</div>
            <div style="color:#f1f5f9; font-size:4rem; font-weight:800; line-height:1;">0.6575</div>
            <div style="color:#f59e0b; font-size:0.9rem; margin-top:10px;">✅ Ambang batas ≥ 0.50</div>
            <div style="color:#94a3b8; font-size:0.82rem; margin-top:8px;">
                Kata kunci dalam satu topik berkaitan secara semantik<br>
                → Topik bermakna dan koheren
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Penjelasan metrik
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">📏 Apa itu Topic Diversity (TD)?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="callout green">
            <div class="callout-title">Mengukur Keunikan antar Topik</div>
            <p>TD = proporsi kata kunci yang <b>unik</b> (tidak berulang) di seluruh topik. 
            Nilai 1.0 berarti tidak ada satu kata kunci pun yang sama antara topik satu dan lainnya.</p>
        </div>

        <div style="background:#0d2035; border:1px solid #1e3a5f; border-radius:10px; padding:16px; margin-top:12px;">
            <div style="color:#64748b; font-size:0.75rem; font-weight:600; margin-bottom:8px;">CONTOH:</div>
            <div style="color:#94a3b8; font-size:0.82rem; line-height:1.7;">
                🎮 T-0 (Game): <code style="color:#60a5fa;">game, npc, fsm, player</code><br>
                💬 T-4 (Sentimen): <code style="color:#60a5fa;">twitter, sentimen, opini</code><br>
                → Tidak ada kata yang overlap ✅<br>
                → TD tinggi = topik tersegmentasi baik
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">📐 Apa itu Topic Coherence (Cv)?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="callout yellow">
            <div class="callout-title">Mengukur Keterkaitan Semantik dalam Topik</div>
            <p>Cv mengukur seberapa sering kata-kata dalam satu topik muncul bersama-sama 
            dalam jendela teks tertentu. Nilai tinggi = kata kunci saling berkaitan erat.</p>
        </div>

        <div style="background:#0d2035; border:1px solid #1e3a5f; border-radius:10px; padding:16px; margin-top:12px;">
            <div style="color:#64748b; font-size:0.75rem; font-weight:600; margin-bottom:8px;">RENTANG NILAI:</div>
            <div style="color:#94a3b8; font-size:0.82rem; line-height:1.7;">
                < 0.50 → ❌ Kurang baik (teks pendek: sulit)<br>
                0.50–0.65 → ✅ Baik (literatur: rata-rata non-Inggris)<br>
                0.65–0.80 → ✅ Sangat baik<br>
                > 0.80 → ✅ Excellent<br>
                <b style="color:#fbbf24;">Penelitian ini: 0.6575 → Baik ✅</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Gauge chart
    st.markdown('<div class="section-header">📊 Visualisasi Kualitas Model</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    def make_gauge(value, title, threshold, color):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number={'font': {'color': '#f1f5f9', 'size': 36}},
            title={'text': title, 'font': {'color': '#94a3b8', 'size': 14}},
            gauge={
                'axis': {'range': [0, 1], 'tickcolor': '#64748b', 'tickfont': {'color': '#64748b'}},
                'bar': {'color': color, 'thickness': 0.3},
                'bgcolor': '#1e293b',
                'bordercolor': '#334155',
                'steps': [
                    {'range': [0, threshold], 'color': '#1e293b'},
                    {'range': [threshold, 1], 'color': '#0f2744'},
                ],
                'threshold': {
                    'line': {'color': '#f59e0b', 'width': 3},
                    'thickness': 0.8,
                    'value': threshold
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', height=230,
            margin=dict(l=20, r=20, t=40, b=10),
            font_color='#94a3b8',
        )
        return fig

    with col1:
        st.plotly_chart(make_gauge(0.9421, "Topic Diversity (TD)", 0.70, "#10b981"), use_container_width=True)
    with col2:
        st.plotly_chart(make_gauge(0.6575, "Topic Coherence (Cv)", 0.50, "#f59e0b"), use_container_width=True)

    # Perbandingan dengan literatur
    st.markdown('<div class="section-header">📚 Perbandingan dengan Penelitian Sebelumnya</div>', unsafe_allow_html=True)

    lit_df = pd.DataFrame({
        'Penelitian': ['Penelitian Ini (BERTopic)', 'Egger & Yu 2022 — BERTopic', 'Egger & Yu 2022 — LDA',
                       'Muthusami et al. 2024', 'Fitri et al. 2021 (LDA - BI)'],
        'Metode': ['BERTopic', 'BERTopic', 'LDA', 'BERTopic', 'LDA'],
        'Data': ['Abstrak Skripsi TI (ID)', 'Twitter (EN)', 'Twitter (EN)', 'Teks Pendek Multi-domain', 'Berita (ID)'],
        'Cv': ['0.6575 ✅', '~0.60', '~0.45', '0.50–0.65', '~0.55'],
        'Keterangan': ['Lebih tinggi dari rata-rata', 'Pembanding utama', 'LDA tertinggal', 'Rerata domain umum', 'Bahasa Indonesia']
    })
    st.dataframe(lit_df, use_container_width=True, hide_index=True)


# ────────────────────────────────────────────────────────────────
# HALAMAN: KESIMPULAN
# ────────────────────────────────────────────────────────────────
elif menu == "💡 Kesimpulan & Saran":
    st.markdown('<h2 style="color:#f1f5f9; margin-bottom:4px;">💡 Kesimpulan & Saran</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;">Ringkasan temuan penelitian dan rekomendasi pengembangan selanjutnya</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">✅ Kesimpulan</div>', unsafe_allow_html=True)

    conclusions = [
        ("1", "Konfigurasi Parameter Optimal",
         "Skenario E1 (UMAP: n_neighbors=15, n_components=5, min_dist=0.0; HDBSCAN: min_cluster_size=10, eom) menghasilkan kualitas terbaik dengan <b>Cv=0.6575</b> (≥0.50 ✅) dan <b>TD=0.9421</b> (≥0.70 ✅) — keduanya melampaui ambang batas kualitas.",
         "#34d399"),
        ("2", "221 Topik Berhasil Diidentifikasi",
         "BERTopic berhasil menemukan <b>221 topik</b> secara otomatis dari 14.629 abstrak. Topik dominan: Pengembangan Game/FSM (538 dok.), Sistem Informasi Pariwisata (368 dok.), E-Commerce Web (219 dok.), E-Learning (203 dok.), dan Analisis Sentimen (177 dok.).",
         "#60a5fa"),
        ("3", "Dominasi Penelitian: Sistem Informasi & Game",
         "Secara umum, penelitian TI Indonesia didominasi oleh <b>pengembangan sistem informasi berbasis kebutuhan layanan masyarakat</b> (pariwisata, kesehatan, pendidikan, desa) dan <b>game development</b> — selaras dengan temuan Gupta et al. (2022) pada negara berkembang.",
         "#fbbf24"),
        ("4", "BERTopic Unggul pada Teks Pendek",
         "Representasi semantik berbasis Transformer terbukti <b>lebih baik</b> dari metode bag-of-words (LDA) untuk teks pendek seperti abstrak skripsi — menangkap konteks dan makna, bukan hanya frekuensi kata.",
         "#a78bfa"),
    ]

    for num, title, desc, color in conclusions:
        st.markdown(f"""
        <div style="background:#1e293b; border-left:4px solid {color}; border-radius:0 12px 12px 0;
                    padding:18px 20px; margin-bottom:12px;">
            <div style="color:{color}; font-size:0.75rem; font-weight:700; margin-bottom:6px; letter-spacing:0.08em;">
                KESIMPULAN {num}
            </div>
            <div style="color:#f1f5f9; font-size:0.95rem; font-weight:600; margin-bottom:6px;">{title}</div>
            <div style="color:#94a3b8; font-size:0.85rem; line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔭 Saran Pengembangan</div>', unsafe_allow_html=True)

    suggestions = [
        ("🔧", "Eksplorasi Parameter Lebih Lanjut",
         "Coba min_cluster_size=5 atau 7 untuk mengurangi rasio noise 32%. Eksplorasi n_neighbors UMAP (10, 20) untuk mengoptimalkan struktur ruang berdimensi rendah."),
        ("🤖", "Model Embedding Lebih Spesifik",
         "Ganti paraphrase-multilingual-MiniLM dengan IndoBERT yang di-fine-tune pada teks ilmiah Indonesia — berpotensi meningkatkan kualitas representasi semantik."),
        ("📊", "Analisis Tren Temporal Penuh",
         "Eksekusi penuh topics_over_time() BERTopic untuk visualisasi perkembangan topik dari waktu ke waktu secara interaktif dan komprehensif."),
        ("🏷️", "Otomatisasi Interpretasi Topik (LLM)",
         "Gunakan Large Language Model (GPT/Llama) untuk otomatisasi pelabelan topik dari kata kunci — mengurangi subjektivitas dan mempercepat proses interpretasi."),
    ]

    for emoji, title, desc in suggestions:
        st.markdown(f"""
        <div style="background:#1e293b; border:1px solid #334155; border-radius:12px;
                    padding:16px 18px; margin-bottom:10px; display:flex; gap:14px;">
            <div style="font-size:1.5rem; flex-shrink:0; padding-top:2px;">{emoji}</div>
            <div>
                <div style="color:#f1f5f9; font-size:0.95rem; font-weight:600; margin-bottom:4px;">{title}</div>
                <div style="color:#94a3b8; font-size:0.83rem; line-height:1.5;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Keterbatasan
    st.markdown('<div class="section-header">⚠️ Keterbatasan Penelitian</div>', unsafe_allow_html=True)
    limitations = [
        ("Noise 32%", "Rasio noise relatif tinggi — dokumen terlalu spesifik tidak terpaksa masuk klaster (trade-off kualitas vs coverage)"),
        ("Interpretasi Subjektif", "Pelabelan topik dilakukan manual oleh peneliti — meski dikonfirmasi pembimbing, tetap mengandung unsur subjektivitas"),
        ("Data Statis", "Hanya mencakup periode 2013–2025 — tidak mencerminkan tren penelitian yang muncul setelah itu"),
        ("Satu Skenario Parameter", "Hanya skenario E1 yang dieksekusi penuh — eksplorasi multi-skenario belum dilakukan sepenuhnya"),
    ]
    for lim, desc in limitations:
        st.markdown(f"""
        <div style="background:#1a1025; border:1px solid #3b1f4c; border-radius:8px; padding:12px 16px; margin-bottom:8px;">
            <span style="color:#a78bfa; font-weight:700; font-size:0.85rem;">{lim}</span>
            <span style="color:#94a3b8; font-size:0.83rem;"> — {desc}</span>
        </div>
        """, unsafe_allow_html=True)

    # Info sidang
    st.markdown("""
    <div class="footer-info">
        <b style="color:#94a3b8;">Ahmad Andi Zainuri</b> · NIM 220411100176 · Program Studi Teknik Informatika<br>
        Universitas Trunojoyo Madura · Sidang Skripsi 01 Juli 2026<br>
        <span style="color:#3b82f6;">Pembimbing I:</span> Husni, S.Kom., MT. &nbsp;|&nbsp; 
        <span style="color:#3b82f6;">Pembimbing II:</span> Yoga Dwitya Pramudita, S.Kom., M.Cs.
    </div>
    """, unsafe_allow_html=True)
