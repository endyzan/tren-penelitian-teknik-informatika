# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# ============================================================
# 1. KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Klasterisasi Topik Skripsi Teknik Informatika",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS kustom
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #555;
    }
    .stSelectbox, .stMultiSelect, .stSlider {
        margin-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #888;
        margin-top: 3rem;
        border-top: 1px solid #eee;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. LOAD DATA (dengan caching dan fallback)
# ============================================================
@st.cache_data
def load_data():
    base_path = "output"
    try:
        df = pd.read_csv(os.path.join(base_path, "df_final.csv"))
    except:
        st.error("File df_final.csv tidak ditemukan. Pastikan berada di folder 'output'.")
        st.stop()
    try:
        trend = pd.read_csv(os.path.join(base_path, "topic_trend_classification.csv"))
    except:
        st.error("File topic_trend_classification.csv tidak ditemukan.")
        st.stop()
    try:
        prop = pd.read_csv(os.path.join(base_path, "topic_proportion_per_year.csv"))
    except:
        st.error("File topic_proportion_per_year.csv tidak ditemukan.")
        st.stop()
    
    # Coba load topic_info (bisa dari topic_info_final.csv atau topic_info.csv)
    topic_info = None
    for fname in ['topic_info_final.csv', 'topic_info.csv']:
        fpath = os.path.join(base_path, fname)
        if os.path.exists(fpath):
            topic_info = pd.read_csv(fpath)
            break
    
    eval_df = None
    if os.path.exists(os.path.join(base_path, "eval_results.csv")):
        eval_df = pd.read_csv(os.path.join(base_path, "eval_results.csv"))
    
    return df, trend, prop, topic_info, eval_df

df, trend, prop, topic_info, eval_df = load_data()

# ============================================================
# 3. PREPARE DATA
# ============================================================
# Pastikan kolom tahun int
df['tahun'] = df['tahun'].astype(int)
prop['tahun'] = prop['tahun'].astype(int)

# Gabungkan label topik ke prop (jika belum ada)
if 'label_topik' not in prop.columns:
    prop = prop.merge(trend[['topic_id', 'label_topik', 'tren']], on='topic_id', how='left')

# Daftar topik valid (bukan outlier)
valid_topics = trend[trend['topic_id'] != -1]['topic_id'].tolist()
valid_topics_df = trend[trend['topic_id'].isin(valid_topics)]

# Kategori unik (dari df_final)
kategori_list = []
if 'kategori_topik' in df.columns:
    kategori_list = df['kategori_topik'].dropna().unique().tolist()
    if 'OUTLIER' in kategori_list:
        kategori_list.remove('OUTLIER')

# Rentang tahun
min_year = int(df['tahun'].min())
max_year = int(df['tahun'].max())

# ============================================================
# 4. SIDEBAR NAVIGASI
# ============================================================
# Buat 3 kolom dengan rasio agar logo berada di tengah
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    st.image("./logo_utm.png", width=120)  # sesuaikan lebar logo

# Teks kampus dan prodi (center)
st.sidebar.markdown(
    "<p style='text-align: center; font-weight: bold; font-size: 1.1rem;'>Universitas Trunodjoyo Madura</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='text-align: center; font-size: 0.95rem; color: #555;'>Teknik Informatika</p>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.title("Navigasi")
st.sidebar.markdown("---")
tab_selected = st.sidebar.radio(
    "Pilih Dashboard",
    [
        "Ringkasan",
        "Tren Topik",
        "Emerging vs Declining",
        "Heatmap Proporsi",
        "Bubble Plot",
        "Stacked Bar",
        "Top-1 per Tahun",
        "Peta Jarak",
        "Eksplorasi Topik",
        "Evaluasi Model"
    ]
)
st.sidebar.markdown("---")
st.sidebar.caption("Dibuat untuk Sidang Skripsi · 1 Juli 2026")
st.sidebar.caption("Ahmad Andi Zainuri · 220411100176")

# ============================================================
# 5. FUNGSI VISUALISASI
# ============================================================

def plot_topic_trend(selected_topics, years_range, mode='proporsi', chart_type='line', show_legend=True):
    """Line, area, atau bar chart proporsi/jumlah topik terpilih per tahun."""
    if not selected_topics:
        return go.Figure()
    
    data = prop[prop['topic_id'].isin(selected_topics)]
    data = data[(data['tahun'] >= years_range[0]) & (data['tahun'] <= years_range[1])]
    if data.empty:
        return go.Figure()
    
    fig = go.Figure()
    for tid in selected_topics:
        sub = data[data['topic_id'] == tid].sort_values('tahun')
        label = trend[trend['topic_id'] == tid]['label_topik'].values[0]
        y_vals = sub['proporsi'] if mode == 'proporsi' else sub['n_docs']
        
        if chart_type == 'line':
            fig.add_trace(go.Scatter(
                x=sub['tahun'], y=y_vals,
                mode='lines+markers',
                name=label,
                hovertemplate='%{x}: %{y:.3f}' if mode=='proporsi' else '%{x}: %{y}'
            ))
        elif chart_type == 'area':
            fig.add_trace(go.Scatter(
                x=sub['tahun'], y=y_vals,
                mode='lines',
                fill='tozeroy',
                name=label,
                hovertemplate='%{x}: %{y:.3f}' if mode=='proporsi' else '%{x}: %{y}'
            ))
        else:  # bar
            fig.add_trace(go.Bar(
                x=sub['tahun'], y=y_vals,
                name=label,
                hovertemplate='%{x}: %{y:.3f}' if mode=='proporsi' else '%{x}: %{y}'
            ))
    
    y_title = 'Proporsi' if mode == 'proporsi' else 'Jumlah Dokumen'
    fig.update_layout(
        title=f"Tren Topik ({mode.capitalize()})",
        xaxis_title='Tahun',
        yaxis_title=y_title,
        legend_title='Topik',
        hovermode='x unified',
        height=500,
        showlegend=show_legend
    )
    return fig

def plot_emerging_declining(tren_filter, years_range):
    """Tampilkan line chart untuk topik emerging atau declining."""
    if tren_filter == 'Emerging':
        topik_ids = valid_topics_df[valid_topics_df['tren'] == 'Emerging']['topic_id'].tolist()
        title = "Topik Emerging (Meningkat)"
        color = '#2ecc71'
    elif tren_filter == 'Declining':
        topik_ids = valid_topics_df[valid_topics_df['tren'] == 'Declining']['topic_id'].tolist()
        title = "Topik Declining (Menurun)"
        color = '#e74c3c'
    else:
        return go.Figure()
    
    if not topik_ids:
        return go.Figure()
    
    data = prop[prop['topic_id'].isin(topik_ids)]
    data = data[(data['tahun'] >= years_range[0]) & (data['tahun'] <= years_range[1])]
    if data.empty:
        return go.Figure()
    
    fig = go.Figure()
    for tid in topik_ids:
        sub = data[data['topic_id'] == tid].sort_values('tahun')
        label = trend[trend['topic_id'] == tid]['label_topik'].values[0]
        fig.add_trace(go.Scatter(
            x=sub['tahun'], y=sub['proporsi'],
            mode='lines+markers',
            name=label,
            line=dict(color=color, width=2),
            hovertemplate='%{x}: %{y:.3f}'
        ))
    fig.update_layout(
        title=title,
        xaxis_title='Tahun',
        yaxis_title='Proporsi',
        legend_title='Topik',
        hovermode='x unified',
        height=450
    )
    return fig

def plot_heatmap(years_range, n_topics=20):
    """Heatmap proporsi topik per tahun (top n_topik berdasarkan total dokumen)."""
    top_topic_ids = trend.nlargest(n_topics, 'n_docs_total')['topic_id'].tolist()
    data = prop[prop['topic_id'].isin(top_topic_ids)]
    data = data[(data['tahun'] >= years_range[0]) & (data['tahun'] <= years_range[1])]
    if data.empty:
        return go.Figure()
    
    pivot = data.pivot_table(index='topic_id', columns='tahun', values='proporsi', fill_value=0)
    pivot = pivot * 100  # dalam persen
    labels = [trend[trend['topic_id']==tid]['label_topik'].values[0] for tid in pivot.index]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=labels,
        colorscale='YlOrRd',
        text=pivot.values.round(1),
        texttemplate='%{text}%',
        hovertemplate='%{y}: %{z:.1f}%'
    ))
    fig.update_layout(
        title=f"Heatmap Proporsi Topik (Top {n_topics} Topik)",
        xaxis_title='Tahun',
        yaxis_title='Topik',
        height=500 + 20 * n_topics,
        xaxis=dict(tickmode='linear')
    )
    return fig

def plot_bubble(tren_filter=None):
    """Bubble plot: slope vs prop_last_year, size=n_docs_total, color=tren."""
    data = valid_topics_df.copy()
    if tren_filter and tren_filter != 'Semua':
        data = data[data['tren'] == tren_filter]
    if data.empty:
        return go.Figure()
    
    color_map = {'Emerging': '#2ecc71', 'Declining': '#e74c3c', 'Stabil': '#3498db'}
    fig = px.scatter(
        data,
        x='slope',
        y='prop_last_year',
        size='n_docs_total',
        color='tren',
        color_discrete_map=color_map,
        hover_name='label_topik',
        text='label_topik',
        title='Slope vs Proporsi Tahun Terakhir (Ukuran = Jumlah Dokumen)',
        labels={'slope': 'Slope', 'prop_last_year': 'Proporsi Tahun Terakhir'},
        size_max=40
    )
    fig.update_traces(textposition='top center', textfont_size=9)
    fig.update_layout(height=500)
    return fig

def plot_stacked_bar(years_range, top_n=15):
    """Stacked bar chart komposisi topik per tahun (top_n topik)."""
    top_topic_ids = trend.nlargest(top_n, 'n_docs_total')['topic_id'].tolist()
    data = prop[prop['topic_id'].isin(top_topic_ids)]
    data = data[(data['tahun'] >= years_range[0]) & (data['tahun'] <= years_range[1])]
    if data.empty:
        return go.Figure()
    
    pivot = data.pivot_table(index='tahun', columns='topic_id', values='proporsi', fill_value=0)
    pivot = pivot.sort_index()
    labels = [trend[trend['topic_id']==tid]['label_topik'].values[0] for tid in pivot.columns]
    
    fig = go.Figure()
    for i, tid in enumerate(pivot.columns):
        fig.add_trace(go.Bar(
            x=pivot.index,
            y=pivot[tid],
            name=labels[i],
            hovertemplate='%{x}: %{y:.3f}'
        ))
    fig.update_layout(
        barmode='stack',
        title=f'Komposisi Topik per Tahun (Top {top_n} Topik)',
        xaxis_title='Tahun',
        yaxis_title='Proporsi',
        height=450,
        legend_title='Topik'
    )
    return fig

def plot_top1_per_year(years_range):
    """Bar chart top-1 topik per tahun."""
    # Gunakan prop langsung, jangan pakai variabel data yang belum didefinisikan
    data_prop = prop[(prop['tahun'] >= years_range[0]) & (prop['tahun'] <= years_range[1])]
    if data_prop.empty:
        return go.Figure()
    top1 = data_prop.sort_values(['tahun', 'proporsi'], ascending=[True, False]).groupby('tahun').first().reset_index()
    if top1.empty:
        return go.Figure()
    fig = px.bar(
        top1,
        x='tahun',
        y='proporsi',
        text='label_topik',
        color='label_topik',
        title='Topik Dominan (Top-1) per Tahun',
        labels={'tahun': 'Tahun', 'proporsi': 'Proporsi'}
    )
    fig.update_traces(textposition='outside', textfont_size=10)
    fig.update_layout(showlegend=True, height=400)
    return fig

# ============================================================
# 6. TAB RINGKASAN
# ============================================================
if tab_selected == "Ringkasan":
    st.markdown('<div class="main-header">Klasterisasi Topik Penelitian Skripsi</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Teknik Informatika · 14.629 Abstrak · 2013–2025</div>', unsafe_allow_html=True)
    
    # Metrik
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-label">Total Abstrak</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        n_topics = len(valid_topics)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{n_topics}</div>
            <div class="metric-label">Jumlah Topik</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        outlier_pct = (df['topic_id'] == -1).mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{outlier_pct:.1f}%</div>
            <div class="metric-label">Outlier</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        if eval_df is not None:
            best = eval_df.iloc[0]
            cv = best['cv_score']
            td = best['td_score']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">Cv {cv:.3f} / TD {td:.3f}</div>
                <div class="metric-label">Topic Coherence / Diversity</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">✅</div>
                <div class="metric-label">Model Siap</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Distribusi Abstrak per Tahun")
        year_dist = df['tahun'].value_counts().sort_index()
        fig = px.bar(x=year_dist.index, y=year_dist.values, labels={'x':'Tahun', 'y':'Jumlah'})
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col_right:
        st.subheader("Distribusi Asal Kampus")
        campus_dist = df['asal_kampus'].value_counts()
        fig = px.bar(x=campus_dist.index, y=campus_dist.values, labels={'x':'Kampus', 'y':'Jumlah'})
        fig.update_layout(showlegend=False, height=300, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("10 Topik Teratas")
    top10 = valid_topics_df.nlargest(10, 'n_docs_total')
    fig = px.bar(top10, x='label_topik', y='n_docs_total',
                 color='n_docs_total', color_continuous_scale='Blues',
                 labels={'n_docs_total': 'Jumlah Dokumen', 'label_topik': 'Topik'})
    fig.update_layout(xaxis_tickangle=-45, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Lihat Semua Topik"):
        st.dataframe(valid_topics_df[['topic_id', 'label_topik', 'n_docs_total', 'slope', 'tren']], use_container_width=True)

# ============================================================
# 7. TAB TREN TOPIK
# ============================================================
elif tab_selected == "Tren Topik":
    st.markdown('<div class="main-header">Tren Topik</div>', unsafe_allow_html=True)
    st.markdown("Gunakan filter di sidebar untuk menyesuaikan grafik.")
    
    # Filter di sidebar
    st.sidebar.subheader("Filter Tren Topik")
    years = st.sidebar.slider("Rentang Tahun", min_year, max_year, (min_year, max_year))
    
    # Pilihan topik
    topik_options = trend[['topic_id', 'label_topik']].drop_duplicates()
    topik_options = topik_options[topik_options['topic_id'] != -1]
    topik_dict = dict(zip(topik_options['label_topik'], topik_options['topic_id']))
    
    # Pilihan filter tambahan
    filter_by = st.sidebar.selectbox("Pilih metode pemilihan topik", 
                                     ["Pilih manual", "Berdasarkan tren", "Berdasarkan kategori", "Top N topik"])
    
    if filter_by == "Pilih manual":
        selected_labels = st.sidebar.multiselect("Pilih Topik", options=list(topik_dict.keys()))
        selected_topics = [topik_dict[l] for l in selected_labels if l in topik_dict]
    elif filter_by == "Berdasarkan tren":
        tren_options = ['Emerging', 'Declining', 'Stabil']
        selected_tren = st.sidebar.multiselect("Tren", tren_options, default=tren_options)
        filtered = valid_topics_df[valid_topics_df['tren'].isin(selected_tren)]
        selected_topics = filtered['topic_id'].tolist()
    elif filter_by == "Berdasarkan kategori":
        if kategori_list:
            selected_kategori = st.sidebar.multiselect("Kategori", kategori_list, default=kategori_list[:3])
            # Ambil topik yang memiliki kategori tersebut
            if 'kategori_topik' in df.columns:
                topic_kategori = df[['topic_id', 'kategori_topik']].drop_duplicates()
                topic_kategori = topic_kategori[topic_kategori['kategori_topik'].isin(selected_kategori)]
                selected_topics = topic_kategori['topic_id'].tolist()
                # Filter hanya yang valid
                selected_topics = [t for t in selected_topics if t in valid_topics]
            else:
                selected_topics = []
        else:
            st.sidebar.warning("Tidak ada kategori tersedia.")
            selected_topics = []
    else:  # Top N topik
        n_top = st.sidebar.slider("Jumlah topik teratas", 5, 50, 20)
        selected_topics = valid_topics_df.nlargest(n_top, 'n_docs_total')['topic_id'].tolist()
    
    # Batasi jumlah topik untuk performa
    if len(selected_topics) > 30:
        st.sidebar.warning(f"Menampilkan 30 dari {len(selected_topics)} topik (gunakan filter lebih spesifik).")
        selected_topics = selected_topics[:30]
    
    # Mode tampilan
    mode = st.sidebar.radio("Tampilkan", ["Proporsi", "Jumlah Absolut"], index=0)
    chart_type = st.sidebar.selectbox("Jenis Grafik", ["Line", "Area", "Bar"], index=0)
    show_legend = st.sidebar.checkbox("Tampilkan Legenda", value=True)
    
    if selected_topics:
        fig = plot_topic_trend(
            selected_topics, years,
            mode='proporsi' if mode=='Proporsi' else 'jumlah',
            chart_type=chart_type.lower(),
            show_legend=show_legend
        )
        if fig.data:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Tidak ada data untuk rentang tahun yang dipilih.")
    else:
        st.warning("Tidak ada topik yang dipilih.")
    
    with st.expander("Topik yang Ditampilkan"):
        if selected_topics:
            display_df = trend[trend['topic_id'].isin(selected_topics)][['topic_id', 'label_topik', 'n_docs_total', 'tren']]
            st.dataframe(display_df, use_container_width=True)

# ============================================================
# 8. TAB EMERGING VS DECLINING
# ============================================================
elif tab_selected == "Emerging vs Declining":
    st.markdown('<div class="main-header">Topik Emerging & Declining</div>', unsafe_allow_html=True)
    st.sidebar.subheader("Filter Emerging/Declining")
    years = st.sidebar.slider("Rentang Tahun", min_year, max_year, (min_year, max_year), key="ed_years")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Emerging (Meningkat)")
        fig = plot_emerging_declining('Emerging', years)
        if fig.data:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada topik Emerging.")
    with col2:
        st.subheader("Declining (Menurun)")
        fig = plot_emerging_declining('Declining', years)
        if fig.data:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada topik Declining.")
    
    with st.expander("Daftar Topik Emerging & Declining"):
        ed_df = valid_topics_df[valid_topics_df['tren'].isin(['Emerging', 'Declining'])][['topic_id', 'label_topik', 'n_docs_total', 'slope', 'p_value', 'tren']]
        st.dataframe(ed_df, use_container_width=True)

# ============================================================
# 9. TAB HEATMAP
# ============================================================
elif tab_selected == "Heatmap Proporsi":
    st.markdown('<div class="main-header">Heatmap Proporsi Topik per Tahun</div>', unsafe_allow_html=True)
    st.sidebar.subheader("Filter Heatmap")
    years = st.sidebar.slider("Rentang Tahun", min_year, max_year, (min_year, max_year), key="heat_years")
    n_topics_heat = st.sidebar.slider("Jumlah Topik", 10, 50, 20, step=5)
    
    fig = plot_heatmap(years, n_topics_heat)
    if fig.data:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada data.")

# ============================================================
# 10. TAB BUBBLE PLOT
# ============================================================
elif tab_selected == "Bubble Plot":
    st.markdown('<div class="main-header">Bubble Plot: Slope vs Proporsi</div>', unsafe_allow_html=True)
    st.sidebar.subheader("Filter Bubble Plot")
    tren_filter = st.sidebar.selectbox("Filter Tren", ["Semua", "Emerging", "Declining", "Stabil"], index=0)
    
    fig = plot_bubble(tren_filter if tren_filter!="Semua" else None)
    if fig.data:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada data.")

# ============================================================
# 11. TAB STACKED BAR
# ============================================================
elif tab_selected == "Stacked Bar":
    st.markdown('<div class="main-header">Komposisi Topik per Tahun (Stacked Bar)</div>', unsafe_allow_html=True)
    st.sidebar.subheader("Filter Stacked Bar")
    years = st.sidebar.slider("Rentang Tahun", min_year, max_year, (min_year, max_year), key="stack_years")
    top_n = st.sidebar.slider("Jumlah Topik", 5, 30, 15)
    
    fig = plot_stacked_bar(years, top_n)
    if fig.data:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada data.")

# ============================================================
# 12. TAB TOP-1 PER TAHUN
# ============================================================
elif tab_selected == "Top-1 per Tahun":
    st.markdown('<div class="main-header">Topik Dominan (Top-1) per Tahun</div>', unsafe_allow_html=True)
    st.sidebar.subheader("Filter Top-1")
    years = st.sidebar.slider("Rentang Tahun", min_year, max_year, (min_year, max_year), key="top1_years")
    
    fig = plot_top1_per_year(years)
    if fig.data:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada data.")

# ============================================================
# 13. TAB PETA JARAK (Embed HTML)
# ============================================================
elif tab_selected == "Peta Jarak":
    st.markdown('<div class="main-header">Inter-Topic Distance Map</div>', unsafe_allow_html=True)
    st.markdown("Visualisasi jarak antar topik berdasarkan embedding (UMAP).")
    
    html_path = "output/vis_final_itd.html"
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=700, scrolling=True)
    else:
        st.warning("File vis_final_itd.html tidak ditemukan. Pastikan sudah dihasilkan dari notebook.")

# ============================================================
# 14. TAB EKSPLORASI TOPIK (DIPERBAIKI)
# ============================================================
elif tab_selected == "Eksplorasi Topik":
    st.markdown('<div class="main-header">Eksplorasi Topik</div>', unsafe_allow_html=True)
    
    # Pilih topik
    topic_options = valid_topics_df[['topic_id', 'label_topik']].drop_duplicates()
    topic_dict = dict(zip(topic_options['label_topik'], topic_options['topic_id']))
    selected_topic_label = st.selectbox("Pilih Topik", options=list(topic_dict.keys()))
    selected_topic_id = topic_dict[selected_topic_label]
    
    # Informasi topik
    topic_info_row = trend[trend['topic_id'] == selected_topic_id].iloc[0]
    st.subheader(f"Topik: {selected_topic_label}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Dokumen", topic_info_row['n_docs_total'])
    col2.metric("Slope", f"{topic_info_row['slope']:.5f}")
    col3.metric("Tren", topic_info_row['tren'])
    col4.metric("P-Value", f"{topic_info_row['p_value']:.4f}")
    
    # Kata kunci - dengan penanganan fleksibel
    st.subheader("Kata Kunci")
    if topic_info is not None:
        words_row = topic_info[topic_info['Topic'] == selected_topic_id]
        if not words_row.empty:
            # Cari kolom yang berisi kata kunci
            keyword_col = None
            for col in ['Representation', 'Words', 'Name']:
                if col in words_row.columns:
                    keyword_col = col
                    break
            if keyword_col:
                keywords = words_row[keyword_col].values[0]
                if isinstance(keywords, str):
                    st.write("**Kata Kunci:**", keywords)
                elif isinstance(keywords, list):
                    st.write("**Kata Kunci:**", ', '.join(keywords))
                else:
                    st.write("**Kata Kunci:**", str(keywords))
            else:
                st.info("Kata kunci tidak tersedia di file topic_info (kolom tidak ditemukan).")
        else:
            st.info("Topik tidak ditemukan di file topic_info.")
    else:
        st.info("File topic_info tidak ditemukan. Kata kunci tidak dapat ditampilkan.")
    
    # Tren topik ini
    st.subheader("Tren Proporsi Topik Ini")
    fig = plot_topic_trend([selected_topic_id], (min_year, max_year), mode='proporsi', chart_type='line')
    if fig.data:
        st.plotly_chart(fig, use_container_width=True)
    
    # Contoh dokumen (5 abstrak acak dari topik ini)
    st.subheader("Contoh Abstrak")
    docs = df[df['topic_id'] == selected_topic_id][['id', 'judul', 'abstrak']].sample(min(5, len(df[df['topic_id'] == selected_topic_id])))
    for _, row in docs.iterrows():
        with st.expander(f"ID {row['id']}: {row['judul'][:60]}..."):
            st.write(row['abstrak'])

# ============================================================
# 15. TAB EVALUASI MODEL
# ============================================================
elif tab_selected == "Evaluasi Model":
    st.markdown('<div class="main-header">Evaluasi Model</div>', unsafe_allow_html=True)
    
    if eval_df is not None:
        st.subheader("Perbandingan Skenario")
        st.dataframe(eval_df[['skenario', 'n_topics', 'pct_clustered', 'cv_score', 'td_score', 'composite_score']], use_container_width=True)
        
        # Plot perbandingan Cv, TD, Composite
        fig = go.Figure()
        fig.add_trace(go.Bar(x=eval_df['skenario'], y=eval_df['cv_score'], name='Cv Score'))
        fig.add_trace(go.Bar(x=eval_df['skenario'], y=eval_df['td_score'], name='TD Score'))
        fig.add_trace(go.Bar(x=eval_df['skenario'], y=eval_df['composite_score'], name='Composite Score'))
        fig.update_layout(
            barmode='group',
            title='Perbandingan Metrik Evaluasi per Skenario',
            xaxis_title='Skenario',
            yaxis_title='Nilai',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Skenario terbaik
        best = eval_df.iloc[0]
        st.success(f"Skenario terbaik: **{best['skenario']}** dengan Composite Score {best['composite_score']:.4f} "
                   f"(Cv={best['cv_score']:.4f}, TD={best['td_score']:.4f})")
    else:
        st.warning("File eval_results.csv tidak ditemukan.")

# ============================================================
# 16. FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    Aplikasi ini dibuat untuk keperluan Sidang Skripsi<br>
    Ahmad Andi Zainuri · 220411100176 · Program Studi Teknik Informatika<br>
    Universitas Trunojoyo Madura · 1 Juli 2026
</div>
""", unsafe_allow_html=True)