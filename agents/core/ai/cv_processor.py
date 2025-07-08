import pytesseract
from pdf2image import convert_from_bytes
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_cv(cv_file):
    if cv_file.name.endswith('.pdf'):
        images = convert_from_bytes(cv_file.read())
        text = " ".join([pytesseract.image_to_string(img) for img in images])
    else:
        text = pytesseract.image_to_string(cv_file)
    return text

def extract_skills(cv_text):
    doc = nlp(cv_text)
    skills = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            skills.append(ent.text)
    return list(set(skills))

def rewrite_cv(job_description, cv_text):
    # AI-powered CV rewriting logic
    # (Simplified example - use transformers in production)
    keywords = extract_keywords(job_description)
    return f"CV optimized for: {', '.join(keywords)}\n\n{cv_text}"
