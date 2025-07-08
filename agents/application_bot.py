from playwright.sync_api import sync_playwright
from core.models import JobListing, JobApplication, UserProfile
import random
import time
from core.ai.cover_letter_generator import generate_cover_letter
import os

def apply_for_job(job, user):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto(job.url, timeout=60000)
            
            # Fill basic information
            page.fill("#name", user.full_name)
            page.fill("#email", user.email)
            
            if user.phone:
                page.fill("#phone", user.phone)
            
            # Upload CV
            if user.optimized_cv_path and os.path.exists(user.optimized_cv_path):
                page.set_input_files("input[type=file]", user.optimized_cv_path)
            
            # Generate and fill cover letter
            cover_letter = generate_cover_letter(job.description, user.cv_text)
            if page.query_selector("#cover_letter"):
                page.fill("#cover_letter", cover_letter)
            
            # Human-like interaction delays
            time.sleep(random.uniform(2, 5))
            
            # Submit application
            page.click("#submit_application")
            
            # Verify submission
            time.sleep(3)
            if "thank you" in page.content().lower() or "success" in page.content().lower():
                return True, cover_letter
            return False, "Submission verification failed"
        
        except Exception as e:
            return False, str(e)
        finally:
            browser.close()

def process_applications():
    user = UserProfile.objects.filter(job_search_active=True).first()
    if not user:
        return
        
    # Get 100 unscraped jobs
    jobs = JobListing.objects.filter(
        applied=False, 
        is_scam=False
    ).order_by('?')[:100]
    
    for job in jobs:
        success, message = apply_for_job(job, user)
        
        JobApplication.objects.create(
            user=user,
            job=job,
            status="SUBMITTED" if success else "FAILED",
            cover_letter=message if not success else "",
            retry_count=1 if not success else 0
        )
        
        job.applied = True
        job.save()
        
        if not success:
            print(f"Application failed for {job.title}: {message}")
        
        # Anti-spam delay
        time.sleep(random.uniform(30, 120))
