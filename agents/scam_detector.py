import re
from core.models import JobListing
from urllib.parse import urlparse
import tldextract
import django

# Initialize Django
django.setup()

# Enhanced scam detection patterns
SCAM_PATTERNS = [
    r"\b(registration fee|pay.*upfront|send.*money|bank.*details)\b",
    r"\b(urgent.*hiring|work from home.*immediately|no experience needed)\b",
    r"\b(earn.*per day|investment.*required|personal information.*required)\b",
    r"\b(wire transfer|western union|money gram|bitcoin payment)\b",
    r"\b(high returns|quick money|double your investment)\b",
    r"\b(no interview|hire.*immediately|start.*today)\b"
]

DOMAIN_BLACKLIST = [
    "jobscam.co.za",
    "fakejobs.co.za",
    "employment-scam.com"
]

def is_suspicious_domain(url):
    """Check if domain is suspicious"""
    domain = urlparse(url).netloc
    extracted = tldextract.extract(domain)
    
    # Check blacklist
    if domain in DOMAIN_BLACKLIST:
        return True, f"Blacklisted domain: {domain}"
    
    # Check for suspicious TLDs
    suspicious_tlds = [".xyz", ".top", ".gq", ".ml", ".cf", ".tk"]
    if any(extracted.suffix in tld for tld in suspicious_tlds):
        return True, f"Suspicious TLD: {extracted.suffix}"
    
    # Check domain age (would require WHOIS lookup in production)
    
    return False, ""

def detect_job_scam(description, url):
    """Detect potential job scams using multiple techniques"""
    # Check for suspicious phrases
    description_lower = description.lower()
    for pattern in SCAM_PATTERNS:
        if re.search(pattern, description_lower):
            return True, f"Matched scam pattern: {pattern}"
    
    # Check for suspicious domains
    is_domain_scam, reason = is_suspicious_domain(url)
    if is_domain_scam:
        return True, reason
    
    # Check for email domains from free providers
    email_matches = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", description)
    for email in email_matches:
        domain = email.split('@')[-1]
        if domain in ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]:
            return True, f"Suspicious email domain: {domain}"
    
    return False, ""

def check_existing_listings():
    """Check existing job listings for scams"""
    unchecked_jobs = JobListing.objects.filter(is_scam=False, scam_checked=False)
    print(f"Found {len(unchecked_jobs)} jobs to check for scams")
    
    for job in unchecked_jobs:
        is_scam, reason = detect_job_scam(job.description, job.url)
        if is_scam:
            print(f"Marking job as scam: {job.title} at {job.company} - Reason: {reason}")
            job.is_scam = True
            job.scam_reason = reason
        job.scam_checked = True
        job.save()

if __name__ == "__main__":
    check_existing_listings()
