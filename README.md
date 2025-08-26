# Resume Analyzer

![Resume Analyzer](https://img.shields.io/badge/Status-Active-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

Welcome to **Resume Analyzer**, a powerful AI-driven tool built with Streamlit to optimize your resume by analyzing it against job descriptions. This application extracts skills, calculates similarity scores, generates visualizations, and provides actionable recommendations to enhance your resume's alignment with job requirements.

## Features
- **PDF and DOCX Support**: Upload resumes in PDF or DOCX format for analysis.
- **Skill Matching**: Identifies matching, missing, and extra skills compared to a job description.
- **Advanced NLP**: Uses spaCy for natural language processing to extract and preprocess text.
- **Visualizations**: Interactive charts (pie and bar) to display skill distribution and comparison.
- **Actionable Insights**: Generates tailored recommendations to improve your resume.
- **Exportable Reports**: Download a summary report of the analysis.

## Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/resume-analyzer.git
   cd resume-analyzer


Set Up a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt
python -m spacy download en_core_web_sm


Run the Application:
streamlit run app.py

Open your browser and navigate to http://localhost:8501.


##Usage

Upload Resume: Use the file uploader to submit your resume (PDF or DOCX, max 200MB).
Input Job Description: Paste the job description into the provided text area.
Analyze: Click "Analyze Resume" to generate insights, metrics, and visualizations.
Review: Check matched skills, missing skills, and recommendations.
Export: Download a report for your records.

##Example

Resume: Upload a DOCX file containing your experience and skills.
Job Description: Paste a job posting text, e.g.:Data Scientist
Tech Innovations Inc.
New York, NY
Job Overview
We are seeking a skilled Data Scientist... [rest of description]


##Output: The app will display a similarity score, skill matches (e.g., Python, SQL), missing skills (e.g., PyTorch), and suggestions.



Built with Streamlit for an interactive UI.
Powered by spaCy for NLP capabilities.
Visualization support from Plotly.

Contact
For questions or support, please open an issue on the GitHub repository or contact the maintainers.
Happy resume optimizing!```
