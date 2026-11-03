# 🎯 SmartJob Matcher: AI Resume & Job Description Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red)
![License](https://img.shields.io/badge/License-MIT-green)

> **Aplikasi AI yang menganalisis kecocokan semantik antara CV dan deskripsi pekerjaan menggunakan Natural Language Processing (NLP), bukan sekadar pencocokan kata kunci.**

---

## 🚀 Fitur Utama
- 🤖 **AI-Powered Analysis**: Menggunakan *Sentence Transformers* untuk memahami makna kontekstual teks.
- 📄 **Dukungan PDF**: Ekstraksi teks otomatis dari file PDF CV.
- 📊 **Smart Scoring**: Skor kecocokan 0-100% dengan interpretasi yang mudah dipahami.
- 🧹 **Text Preprocessing**: Pembersihan teks otomatis (regex) untuk hasil ekstraksi PDF yang lebih akurat.
- 🎨 **Clean UI**: Antarmuka web yang responsif dan intuitif dibangun dengan Streamlit.

---

## 🛠️ Tech Stack
| Komponen | Teknologi |
|----------|-----------|
| **Backend AI** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **NLP** | Text Embeddings, Cosine Similarity |
| **Data Processing** | PyPDF2, Regular Expression (Regex) |
| **Web Framework** | Streamlit |
| **Version Control** | Git & GitHub |

---

## 📦 Cara Menjalankan (Installation)

Pastikan kamu sudah menginstal Python 3.9+ di komputermu.

```bash
# 1. Clone repository ini
git clone https://github.com/angelinayessyca01/smartjob-matcher.git
cd smartjob-matcher

# 2. Buat dan aktifkan virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py