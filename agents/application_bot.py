from playwright.sync_api import sync_playwright
from core.models import JobApplication, UserProfile
import random
import time

def apply_for_job(job, user):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto(job.url)
        page.fill("#applicant_name", user.full_name)
        page.fill("#email", user.email)
        page.fill("#phone", user.phone)
        
        # Upload optimized CV
        page.set_input_files("#resume", user.optimized_cv_path)
        
        # Generate cover letter
        cover_letter = generate_cover_letter(job.description, user.cv_text)
        page.fill("#cover_letter", cover_letter)
        
        # Human-like delay
        time.sleep(random.uniform(5, 15))
        
        page.click("#submit_application")
        
        # Save application record
        JobApplication.objects.create(
            user=user,
            job=job,
            status="SUBMITTED",
            cover_letter=cover_letter
        )
        
        browser.close()

if __name__ == "__main__":
    # Get 100 eligible jobs
    jobs = JobListing.objects.filter(applied=False)[:100]
    user = UserProfile.objects.first()
    
    for job in jobs:
        apply_for_job(job, user)
        time.sleep(random.uniform(30, 120))  # Anti-spam delay
