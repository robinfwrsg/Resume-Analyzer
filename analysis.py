from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from .nlp_processing import preprocess_text  # Import preprocess_text

# Skills database
SKILLS_DATABASE = [
    "python", "java", "javascript", "c++", "c#", "php", "ruby", "go", "rust", "swift",
    "kotlin", "scala", "r", "matlab", "perl", "shell scripting", "bash", "powershell",
    "html", "css", "react", "angular", "vue.js", "node.js", "express.js", "django",
    "flask", "spring boot", "asp.net", "laravel", "ruby on rails", "fastapi",
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis", "cassandra",
    "elasticsearch", "neo4j", "dynamodb", "firestore",
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes", "jenkins", "git",
    "github", "gitlab", "terraform", "ansible", "chef", "puppet", "ci/cd",
    "machine learning", "deep learning", "artificial intelligence", "tensorflow",
    "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "tableau", "power bi", "jupyter", "data analysis", "statistics", "nlp",
    "android", "ios", "react native", "flutter", "xamarin", "ionic",
    "excel", "microsoft office", "google workspace", "jira", "confluence", "slack",
    "agile", "scrum", "kanban", "project management", "leadership", "teamwork",
    "communication", "problem solving", "critical thinking"
]

def extract_skills(text, skills_db=SKILLS_DATABASE):
    """Extract skills from text using dictionary matching"""
    text_lower = text.lower()
    found_skills = set()
    for skill in skills_db:
        skill_variations = [skill, skill.replace(" ", ""), skill.replace(".", "")]
        if any(variation in text_lower for variation in skill_variations):
            found_skills.add(skill)
    return list(found_skills)

def calculate_similarity(resume_text, jd_text):
    """Calculate cosine similarity between resume and job description"""
    try:
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        vectors = vectorizer.fit_transform([resume_text, jd_text])
        return round(cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100, 2)
    except Exception as e:
        st.error(f"❌ Error calculating similarity: {str(e)}")
        return 0

def analyze_resume(resume_text, jd_text, nlp):
    """Analyze resume against job description"""
    resume_tokens, resume_clean = preprocess_text(resume_text, nlp)
    jd_tokens, jd_clean = preprocess_text(jd_text, nlp)
    
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))
    extra_skills = list(set(resume_skills) - set(jd_skills))
    
    similarity_score = calculate_similarity(resume_clean, jd_clean)
    skill_match_percentage = round((len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0, 2)
    
    return {
        'similarity_score': similarity_score,
        'skill_match_percentage': skill_match_percentage,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'extra_skills': extra_skills,
        'resume_skills': resume_skills,
        'jd_skills': jd_skills
    }

def generate_recommendations(analysis_results):
    """Generate improvement recommendations"""
    recommendations = []
    score = analysis_results['similarity_score']
    skill_match = analysis_results['skill_match_percentage']
    missing_skills = analysis_results['missing_skills']
    
    if score < 50:
        recommendations.append("🔴 Low alignment with job description. Restructure your resume to highlight relevant experience.")
    elif score < 70:
        recommendations.append("🟡 Moderate alignment. Enhance your resume to better match job requirements.")
    else:
        recommendations.append("🟢 Strong alignment with job description!")
    
    if skill_match < 40:
        recommendations.append(f"📚 Missing {len(missing_skills)} key skills. Consider relevant courses or showcasing transferable skills.")
    elif skill_match < 70:
        recommendations.append("💪 Develop skills in missing areas to strengthen your profile.")
    
    if missing_skills:
        recommendations.append(f"🎯 Priority skills to develop: {', '.join(missing_skills[:5])}")
    
    if len(analysis_results['extra_skills']) > len(missing_skills):
        recommendations.append("✂️ Remove less relevant skills to focus on targeted content.")
    
    return recommendations