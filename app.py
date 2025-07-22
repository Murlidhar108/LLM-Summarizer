import streamlit as st
from utils import (
    extract_text_from_uploaded_file,
    extract_text_from_path,
    summarize_with_gemini  # 👈 update here
)

st.set_page_config(page_title="PDF Resume Summarizer", layout="centered")
st.title("📄 Resume PDF Summarizer")

uploaded_file = st.file_uploader("📤 Upload a PDF file", type="pdf")
local_path = st.text_input("📁 Or enter a local PDF file path (optional)")

# ---------- Extract Text Button ----------
if st.button("📄 Extract Text"):
    if uploaded_file:
        extracted_text, error_msg = extract_text_from_uploaded_file(uploaded_file)
    elif local_path.strip():
        extracted_text, error_msg = extract_text_from_path(local_path.strip())
    else:
        st.warning("⚠️ Please upload a PDF or enter a valid path.")
        st.stop()

    if error_msg:
        st.error(error_msg)
    elif extracted_text.strip():
        st.success("✅ Text extracted successfully!")
        print("text extracted")
        st.session_state["extracted_text"] = extracted_text
        st.text_area("📃 Extracted Text", extracted_text, height=400)
    else:
        st.warning("⚠️ No readable text found.")

# ---------- Summarize Button ----------
if "extracted_text" in st.session_state:
    if st.button("🧠 Generate Summary"):
        with st.spinner("Summarizing using Gemini..."):
            summary = summarize_with_gemini(st.session_state["extracted_text"])
        st.subheader("📝 Summary")
        st.write(summary)