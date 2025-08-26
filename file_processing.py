import streamlit as st
import PyPDF2
from docx import Document

def extract_text(file, file_type):
    """Extract text from PDF or DOCX file"""
    try:
        if file_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(file)
            return "".join(page.extract_text() + " " for page in pdf_reader.pages).strip()
        else:
            doc = Document(file)
            return "".join(paragraph.text + " " for paragraph in doc.paragraphs).strip()
    except Exception as e:
        st.error(f"❌ Error reading {file_type.split('/')[-1].upper()}: {str(e)}")
        return ""