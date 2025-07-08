import re
import spacy
from urllib.parse import urlparse

nlp = spacy.load("en_core_web_sm")

SCAM_INDICATORS = [
    r"registration fee",
    r"pay.*upfront",
    r"send.*money",
    r"bank.*details",
    r"urgent.*hiring",
    r"work from home.*immediately",
    r"no experience needed",
    r"earn.*per day",
    r"investment.*required",
    r"personal information.*required"
]

def detect_scam(job_description):
    """
    Detect potential job scams using NLP and pattern matching
    Returns: (is_scam, reason)
    """
    if not job_description:
        return False, ""
    
    # Check for scam indicators
    description = job_description.lower()
    for pattern in SCAM_INDICATORS:
        if re.search(pattern, description):
            return True, f"Matched scam pattern: {pattern}"
    
    # Check for suspicious domains
    doc = nlp(description)
    for ent in doc.ents:
        if ent.label_ == "URL":
            domain = urlparse(ent.text).netloc
            if domain.count('.') > 2 or "job" not in domain:
                return True, f"Suspicious domain: {domain}"
    
    return False, ""
