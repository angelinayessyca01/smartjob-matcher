import streamlit as st
from sentence_transformers import SentenceTransformer, util
import PyPDF2
import io
import re

# === KONFIGURASI HALAMAN ===
st.set_page_config(page_title="SmartJob Matcher", page_icon="🎯")

# === TITLE DAN DESKRIPSI ===
st.title("🎯 SmartJob Matcher")
st.markdown("""
**Analisis kecocokan antara CV dan Job Description menggunakan AI**

Aplikasi ini menggunakan Natural Language Processing (NLP) untuk:
- Menganalisis kesamaan semantik antara CV dan lowongan kerja
- Memberikan skor kecocokan (0-100%)
- Membantu kamu optimasi CV agar lebih ATS-friendly
""")


# === LOAD MODEL AI ===
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# === FUNGSI EXTRACT TEKS DARI PDF ===
def extract_text_from_pdf(pdf_file):
    """Fungsi untuk mengekstrak teks dari file PDF"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n\n"
    return text


# === FUNGSI BERSIHKAN TEKS ===
def clean_text(text):
    """Membersihkan teks dari spasi ganda, enter berlebihan, dll"""
    text = re.sub(r" +", " ", text)  # Ganti spasi ganda jadi 1 spasi
    text = re.sub(r"\n{3,}", "\n\n", text)  # Ganti 3+ enter jadi maksimal 2 enter
    lines = [
        line.strip() for line in text.split("\n")
    ]  # Hapus spasi di awal/akhir baris
    text = "\n".join(lines)
    return text.strip()


# === FUNGSI TAMPILKAN STATISTIK & PREVIEW ===
def display_pdf_stats(text, text_type):
    """Fungsi helper untuk menampilkan statistik dan preview teks"""
    word_count = len(text.split())
    line_count = text.count("\n") + 1

    # Tampilkan statistik dalam 3 kolom kecil
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("📝 Karakter", len(text))
    with col_stats2:
        st.metric("📊 Kata", word_count)
    with col_stats3:
        st.metric("📄 Baris", line_count)

    # Preview teks
    with st.expander(f"👁️ Lihat teks yang di-extract dari {text_type}", expanded=False):
        st.markdown("---")
        preview = text[:500] + "..." if len(text) > 500 else text
        st.markdown("**Preview (500 karakter pertama):**")
        st.text(preview)
        st.markdown("---")

        if st.button(f"📖 Lihat TEKS LENGKAP ({text_type})"):
            st.text(text)

    st.success(
        f"✅ {text_type} berhasil dibaca! ({len(text)} karakter, {word_count} kata)"
    )


# === PILIHAN METODE INPUT (DI ATAS KOLOM) ===
st.markdown("###  Metode Input")
col_method1, col_method2 = st.columns(2)

with col_method1:
    cv_input_method = st.radio(
        "📄 CV Input:",
        ["Paste teks", "Upload PDF"],
        key="cv_method",
        horizontal=True,
        label_visibility="collapsed",
    )

with col_method2:
    jd_input_method = st.radio(
        "💼 Job Description Input:",
        ["Paste teks", "Upload PDF"],
        key="jd_method",
        horizontal=True,
        label_visibility="collapsed",
    )

st.markdown("---")

# === LAYOUT: DUA KOLOM UTAMA ===
col1, col2 = st.columns(2)

# === KOLOM 1: CV INPUT ===
with col1:
    st.subheader("📄 Input CV Kamu")

    cv_text = ""

    if cv_input_method == "Paste teks":
        cv_text = st.text_area(
            "Paste teks CV kamu di sini:",
            height=350,
            placeholder="Contoh: Saya adalah lulusan Teknik Informatika dengan pengalaman 2 tahun sebagai software developer...",
            key="cv_textarea",
            label_visibility="collapsed",
        )
    else:  # Upload PDF
        uploaded_cv_file = st.file_uploader(
            "Upload file PDF CV kamu:",
            type=["pdf"],
            key="cv_uploader",
            label_visibility="collapsed",
        )

        if uploaded_cv_file is not None:
            with st.spinner(" Membaca PDF CV..."):
                raw_text = extract_text_from_pdf(uploaded_cv_file)
                cv_text = clean_text(raw_text)

            # Tampilkan statistik dan preview
            display_pdf_stats(cv_text, "CV")

# === KOLOM 2: JOB DESCRIPTION INPUT ===
with col2:
    st.subheader("💼 Job Description")

    job_text = ""

    if jd_input_method == "Paste teks":
        job_text = st.text_area(
            "Paste deskripsi pekerjaan di sini:",
            height=350,
            placeholder="Contoh: Dicari: Software Engineer dengan keahlian Python dan JavaScript...",
            key="jd_textarea",
            label_visibility="collapsed",
        )
    else:  # Upload PDF
        uploaded_jd_file = st.file_uploader(
            "Upload file PDF Job Description:",
            type=["pdf"],
            key="jd_uploader",
            label_visibility="collapsed",
        )

        if uploaded_jd_file is not None:
            with st.spinner("📖 Membaca PDF Job Description..."):
                raw_text = extract_text_from_pdf(uploaded_jd_file)
                job_text = clean_text(raw_text)

            # Tampilkan statistik dan preview
            display_pdf_stats(job_text, "Job Description")

# === TOMBOL ANALISIS ===
st.markdown("---")
analyze_button = st.button(
    " Analisis Kecocokan", type="primary", use_container_width=True, icon="🎯"
)

# === LOGIKA ANALISIS ===
if analyze_button:
    # Validasi input
    if not cv_text.strip():
        st.error("⚠️ CV kosong! Mohon paste teks CV atau upload file PDF.")
    elif not job_text.strip():
        st.error("⚠️ Job Description kosong! Mohon isi deskripsi pekerjaan.")
    else:
        with st.spinner(" AI sedang menganalisis..."):
            # Convert teks ke embedding
            cv_embedding = model.encode(cv_text)
            job_embedding = model.encode(job_text)

            # Hitung cosine similarity
            similarity_score = util.cos_sim(cv_embedding, job_embedding).item()
            percentage = similarity_score * 100

        # === TAMPILKAN HASIL ===
        st.markdown("### 📊 Hasil Analisis")

        # Tampilkan skor dengan metric besar
        st.metric(label="Skor Kecocokan", value=f"{percentage:.1f}%")

        # Berikan interpretasi skor dengan emoji dan warna
        if percentage >= 80:
            st.success(
                "🎉 **Sangat Cocok!** CV kamu sangat sesuai dengan lowongan ini."
            )
        elif percentage >= 60:
            st.info("👍 **Cukup Cocok.** CV kamu relevan, tapi bisa dioptimasi lagi.")
        elif percentage >= 40:
            st.warning(
                "⚠️ **Kurang Cocok.** Pertimbangkan untuk menyesuaikan CV dengan keywords dari job description."
            )
        else:
            st.error(
                "❌ **Tidak Cocok.** CV dan lowongan ini sangat berbeda. Mungkin perlu pivot karir atau update skill."
            )

        # Tampilkan detail teknis
        with st.expander("🔬 Detail Teknis (untuk Developer)"):
            st.code(f"""
Model: all-MiniLM-L6-v2
Metode: Sentence Transformers + Cosine Similarity
Panjang teks CV: {len(cv_text)} karakter
Panjang teks Job Description: {len(job_text)} karakter
Raw Similarity Score: {similarity_score:.6f}
            """)
