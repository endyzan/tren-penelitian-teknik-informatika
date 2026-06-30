# 🎓 Presentasi Sidang Skripsi — BERTopic

**Klasterisasi Topik Penelitian Teknik Informatika Berbasis Abstrak Skripsi Menggunakan BERTopic**

**Ahmad Andi Zainuri · 220411100176 · Universitas Trunojoyo Madura**

---

## 📋 Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Streamlit
```bash
streamlit run app.py
```

Atau akses langsung di browser: `http://localhost:8501`

---

## 📑 Halaman Presentasi

| Halaman | Konten |
|---------|--------|
| 🏠 Beranda & Ringkasan | Overview penelitian, metrik utama, distribusi topik |
| 📊 Data & Preprocessing | Distribusi data per kampus, pipeline preprocessing 2 layer |
| 🧠 Arsitektur BERTopic | Pipeline SBERT → UMAP → HDBSCAN → c-TF-IDF |
| 🔬 Hasil Klasterisasi | 221 topik, 10 topik dominan dengan keyword |
| 📈 Analisis Tren Topik | Emerging / Declining / Stabil berdasarkan regresi linear |
| 🏆 Evaluasi Model | Cv=0.6575, TD=0.9421 dengan gauge chart |
| 💡 Kesimpulan & Saran | Kesimpulan, keterbatasan, dan saran pengembangan |

---

## 🔑 Highlight Hasil Penelitian
- **14.629 abstrak** dari 10 perguruan tinggi (2013–2025)
- **221 topik** terbentuk secara otomatis
- **Topic Diversity: 0.9421** ✅ (≥ 0.70)
- **Topic Coherence: 0.6575** ✅ (≥ 0.50)
- Topik dominan: Game/FSM, Pariwisata, E-Commerce, E-Learning, Sentimen
