import streamlit as st
import spacy
import re

@st.cache_resource
def load_nlp_model():
    """Load spaCy NLP model"""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.error("⚠️ spaCy English model not found! Please run: `python -m spacy download en_core_web_sm`")
        st.stop()

def preprocess_text(text, nlp):
    """Clean and preprocess text"""
    text = re.sub(r'[^a-zA-Z0-9\s+#.]', ' ', text.lower())
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop and len(token.lemma_) > 2]
    return tokens, text