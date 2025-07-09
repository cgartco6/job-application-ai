import imaplib
import email
from email.header import decode_header
import re
from core.models import JobApplication, UserProfile
import django
from datetime import datetime

# Initialize Django
django.setup()

# Email configuration
EMAIL = "your@email.com"
PASSWORD = "yourpassword"
IMAP_SERVER = "imap.gmail.com"

def decode_text(text):
    """Decode encoded email text"""
    if isinstance(text, bytes):
        return text.decode("utf-8", errors="ignore")
    return text

def check_email_for_offers():
    """Check email for job offers and interview requests"""
    print("Checking email for job offers...")
    
    # Connect to email server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    
    # Search for relevant emails
    status, messages = mail.search(None, '(OR SUBJECT "job offer" SUBJECT "interview" SUBJECT "employment")')
    if status != "OK":
        print("Error searching emails")
        return
        
    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} relevant emails")
    
    offer_keywords = ["job offer", "employment offer", "congratulations"]
    interview_keywords = ["interview", "meeting invitation"]
    
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            continue
            
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Decode subject
        subject = ""
        if msg["Subject"]:
            decoded = decode_header(msg["Subject"])[0]
            subject = decode_text(decoded[0])
        
        # Get sender
        sender = msg.get("From", "")
        
        # Extract body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = decode_text(part.get_payload(decode=True))
                    break
        else:
            body = decode_text(msg.get_payload(decode=True))
        
        # Check for job offer
        is_offer = any(keyword in subject.lower() or keyword in body.lower() for keyword in offer_keywords)
        is_interview = any(keyword in subject.lower() or keyword in body.lower() for keyword in interview_keywords)
        
        if is_offer or is_interview:
            # Extract job title and company from email
            job_title = extract_job_title(subject, body)
            company = extract_company(sender)
            
            # Find matching application
            applications = JobApplication.objects.filter(
                job__title__icontains=job_title,
                job__company__icontains=company
            )
            
            if applications:
                application = applications[0]
                if is_offer:
                    print(f"Job offer found for application: {application.job.title}")
                    application.status = "OFFER_RECEIVED"
                    application.user.job_search_active = False
                    application.user.save()
                elif is_interview:
                    print(f"Interview request found for application: {application.job.title}")
                    application.status = "INTERVIEW_SCHEDULED"
                
                application.save()
    
    mail.logout()

def extract_job_title(subject, body):
    """Extract job title from email content"""
    # Look for patterns like "Job Offer: [Position]"
    title_match = re.search(r"Job Offer: (.+?) at", subject)
    if title_match:
        return title_match.group(1)
    
    # Look in body
    body_match = re.search(r"position of (.+?) at", body)
    if body_match:
        return body_match.group(1)
    
    return "Unknown Position"

def extract_company(sender):
    """Extract company name from sender email"""
    # Look for company name in email address
    company_match = re.search(r"@([\w]+)\.", sender)
    if company_match:
        return company_match.group(1).capitalize()
    
    # Look for company name in sender string
    name_match = re.search(r"\((.+?)\)", sender)
    if name_match:
        return name_match.group(1)
    
    return "Unknown Company"

if __name__ == "__main__":
    check_email_for_offers()
