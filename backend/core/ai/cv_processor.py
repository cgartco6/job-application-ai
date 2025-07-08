import pytesseract
from pdf2image import convert_from_bytes
import spacy
import re
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

nlp = spacy.load("en_core_web_sm")

def extract_text_from_cv(cv_file):
    """Extract text from various CV formats"""
    try:
        if cv_file.name.lower().endswith('.pdf'):
            images = convert_from_bytes(cv_file.read())
            text = " ".join([pytesseract.image_to_string(img) for img in images])
        elif cv_file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            text = pytesseract.image_to_string(cv_file)
        else:  # Assume text-based file
            text = cv_file.read().decode('utf-8')
        return text
    except Exception as e:
        print(f"CV processing error: {e}")
        return ""

def extract_skills(cv_text):
    """Extract skills from CV text using NLP"""
    doc = nlp(cv_text)
    skills = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            skills.append(ent.text)
    return list(set(skills))

def rewrite_cv_for_job(cv_text, job_description):
    """Optimize CV text for a specific job description"""
    # Extract keywords from job description
    job_doc = nlp(job_description)
    keywords = [token.lemma_ for token in job_doc 
                if not token.is_stop and token.is_alpha and len(token) > 2]
    
    # Enhance CV with relevant keywords
    cv_doc = nlp(cv_text)
    enhanced_sections = []
    
    for sent in cv_doc.sents:
        # Add keywords to relevant sections
        if any(keyword in sent.text.lower() for keyword in keywords):
            enhanced = sent.text
            for keyword in set(keywords) - set(sent.text.lower().split()):
                if keyword not in enhanced:
                    enhanced += f" • {keyword.capitalize()}"
            enhanced_sections.append(enhanced)
        else:
            enhanced_sections.append(sent.text)
    
    return "\n\n".join(enhanced_sections)
