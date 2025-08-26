import streamlit as st
from utils.file_processing import extract_text
from utils.nlp_processing import load_nlp_model, preprocess_text
from utils.analysis import analyze_resume, generate_recommendations
from utils.visualization import create_skill_charts

# Configure Streamlit page
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("styles/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def display_skills(title, skills, tag_class="skill-tag"):
    """Display skills with styled tags"""
    st.markdown(f'<div class="subheader">{title}</div>', unsafe_allow_html=True)
    if skills:
        for skill in skills[:10]:  # Limit to 10 skills
            st.markdown(f'<span class="{tag_class}">{skill.title()}</span>', unsafe_allow_html=True)
    else:
        st.info("No skills found" if tag_class == "skill-tag" else "All required skills found!")

def main():
    """Main application function"""
    st.markdown('<h1 class="main-header">📄 Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("Optimize your resume with AI-powered analysis, skill matching, and actionable insights.")

    # Load NLP model
    nlp = load_nlp_model()

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("📋 How to Use")
        st.markdown("""
        1. Upload your resume (PDF/DOCX)
        2. Paste the job description
        3. Click 'Analyze Resume'
        4. Review insights and recommendations
        """)
        st.header("🛠️ Features")
        st.markdown("""
        - PDF & DOCX support
        - Advanced NLP analysis
        - Skills matching
        - Interactive charts
        - Actionable recommendations
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Input section
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="subheader">📄 Upload Resume</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose your resume", type=['pdf', 'docx'])
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")

    with col2:
        st.markdown('<div class="subheader">📝 Job Description</div>', unsafe_allow_html=True)
        jd_text = st.text_area("Paste job description", height=150, placeholder="Paste the full job description...")

    # Analysis
    if st.button("🔍 Analyze Resume", type="primary"):
        if not uploaded_file or not jd_text.strip():
            st.error("⚠️ Please upload a resume and provide a job description!")
            return

        with st.spinner("🔄 Analyzing..."):
            resume_text = extract_text(uploaded_file, uploaded_file.type)
            if not resume_text:
                return

            results = analyze_resume(resume_text, jd_text, nlp)

            # Metrics
            st.markdown('<div class="subheader">📊 Key Metrics</div>', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Overall Match", f"{results['similarity_score']}%", delta=f"{results['similarity_score'] - 50:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Skills Match", f"{results['skill_match_percentage']}%", delta=f"{len(results['matched_skills'])} found")
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Resume Skills", len(results['resume_skills']), delta=f"{len(results['matched_skills'])} relevant")
                st.markdown('</div>', unsafe_allow_html=True)
            with col4:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Missing Skills", len(results['missing_skills']), delta="Develop these")
                st.markdown('</div>', unsafe_allow_html=True)

            # Skills analysis
            col1, col2 = st.columns([1, 1])
            with col1:
                display_skills("✅ Matched Skills", results['matched_skills'])
                display_skills("🔍 Extra Skills", results['extra_skills'])
            with col2:
                display_skills("⚠️ Missing Skills", results['missing_skills'], "missing-skill-tag")
                display_skills("📋 JD Skills", results['jd_skills'])

            # Visualizations
            st.markdown('<div class="subheader">📈 Visualizations</div>', unsafe_allow_html=True)
            pie_chart, bar_chart = create_skill_charts(results)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(pie_chart, use_container_width=True)
            with col2:
                st.plotly_chart(bar_chart, use_container_width=True)

            # Recommendations
            st.markdown('<div class="subheader">💡 Recommendations</div>', unsafe_allow_html=True)
            for i, rec in enumerate(generate_recommendations(results), 1):
                st.markdown(f'<div class="recommendation">{i}. {rec}</div>', unsafe_allow_html=True)

            # Export report
            st.markdown('<div class="subheader">📥 Export Report</div>', unsafe_allow_html=True)
            report = f"""
# Resume Analysis Report

## Summary
- Overall Match: {results['similarity_score']}%
- Skills Match: {results['skill_match_percentage']}%
- Resume Skills: {len(results['resume_skills'])}
- Matched Skills: {len(results['matched_skills'])}
- Missing Skills: {len(results['missing_skills'])}

## Matched Skills
{', '.join(results['matched_skills']) or 'None'}

## Missing Skills
{', '.join(results['missing_skills']) or 'None'}

## Recommendations
{chr(10).join(f"{i+1}. {rec}" for i, rec in enumerate(generate_recommendations(results)))}
            """
            st.download_button(
                label="📄 Download Report",
                data=report,
                file_name=f"resume_analysis_{uploaded_file.name.split('.')[0]}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()