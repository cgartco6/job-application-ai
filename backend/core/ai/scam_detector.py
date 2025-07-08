import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def detect_scam(description):
    scam_keywords = [
        'registration fee', 'admin fee', 'processing fee', 
        'pay to apply', 'money transfer', 'western union', 
        'moneygram', 'bitcoin', 'cryptocurrency', 'urgent hiring',
        'work from home', 'no experience', 'earn big'
    ]
    
    # Check for common scam patterns
    for keyword in scam_keywords:
        if keyword in description.lower():
            return True, f"Contains scam keyword: {keyword}"
    
    # Check for excessive urgency
    words = word_tokenize(description.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    urgent_words = ['urgent', 'immediate', 'asap', 'fast', 'quick']
    urgent_count = sum(1 for word in filtered_words if word in urgent_words)
    if urgent_count > 3:
        return True, "Excessive urgency indicators"
    
    return False, None
