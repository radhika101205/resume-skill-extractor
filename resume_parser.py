


# %%
import spacy
import nltk
import PyPDF2
import streamlit
import pandas as pd


# %%
import spacy
spacy.cli.download("en_core_web_sm")


# %%
nlp = spacy.load("en_core_web_sm")
import re

from PyPDF2 import PdfReader
def extract_text_from_pdf(uploaded_file):
    # uploaded_file is a file-like object from Streamlit
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# %%
# Technical skills database
TECHNICAL_SKILLS = {
    'programming': ['python', 'java', 'javascript', 'c++', 'sql'],
    'ml_frameworks': ['tensorflow', 'pytorch', 'scikit-learn', 'keras'],
    'data_tools': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'tableau'],
    'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes']
}

def extract_skills(text, skills_dict):
    found_skills = []
    text_lower = text.lower()
    for category, skills in skills_dict.items():
        for skill in skills:
            if skill in text_lower:
                found_skills.append((skill, category))
    return found_skills


# %%
def extract_entities(text):
    doc = nlp(text)
    entities = {
        'persons': [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
        'organizations': [ent.text for ent in doc.ents if ent.label_ == "ORG"],
        'dates': [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    }
    return entities

def analyze_experience_level(text):
    experience_indicators = {
        'entry': ['intern', 'graduate', 'fresher', 'entry-level'],
        'mid': ['2+ years', '3+ years', 'experienced'],
        'senior': ['senior', 'lead', 'manager', '5+ years', 'architect']
    }

# %%
def identify_resume_sections(text):
    sections = {
        'education': extract_education(text),
        'experience': extract_work_experience(text),
        'projects': extract_projects(text),
        'skills': extract_skills(text, TECHNICAL_SKILLS),
        'certifications': extract_certifications(text)
    }
    return sections


def extract_education(text):
    education_patterns = [
        r"(B\.?Tech|Bachelor|Master|M\.?Tech|MBA|PhD)",
        r"(Computer Science|Engineering|Data Science|Mathematics)"
    ]
    education_info = []
    for pattern in education_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        education_info.extend(matches or [])
    return list(set(education_info))  # Remove duplicates

def extract_work_experience(text):
    experience_patterns = [
        r"(\d+[\+]? years? experience)",
        r"(worked at [A-Za-z0-9\s]+)",
        r"(experience in [A-Za-z0-9\s]+)"
    ]
    experience_info = []
    for pattern in experience_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        experience_info.extend(matches or [])
    return list(set(experience_info))

def extract_projects(text):
    project_patterns = [
        r"(project: [^\n]+)",
        r"(developed [^\n]+)",
        r"(built [^\n]+)"
    ]
    projects = []
    for pattern in project_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        projects.extend(matches or [])
    return list(set(projects))

def extract_certifications(text):
    certification_keywords = ["certification", "certified", "credential", "completed"]
    return [line.strip() for line in text.split("\n") if any(kw in line.lower() for kw in certification_keywords)]

    


# %%
import streamlit as st
import json

def main():
    st.title("Resume Skill Extractor")
    
    uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
    
    if uploaded_file is not None:
        # Process uploaded file
        text = extract_text_from_pdf(uploaded_file)
        
        # Extract information
        skills = extract_skills(text, TECHNICAL_SKILLS)
        entities = extract_entities(text)
        sections = identify_resume_sections(text)
        
        # Display results
        st.subheader("Extracted Skills")
        st.json(skills)
        
        st.subheader("Resume Analysis")
        st.json(sections)
        
        # Generate structured output
        resume_data = {
            'candidate_name': entities['persons'][0] if entities['persons'] else 'Unknown',
            'technical_skills': skills,
            'experience_level': analyze_experience_level(text),
            'education': sections['education'],
            'projects': sections['projects']
        }
        
        st.download_button(
            "Download Parsed Resume Data",
            json.dumps(resume_data, indent=2),
            file_name="parsed_resume.json"
        )

if __name__ == "__main__":
    main()



