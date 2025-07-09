from playwright.sync_api import sync_playwright
from core.models import JobListing, JobApplication, UserProfile
from core.ai.cover_letter_generator import generate_cover_letter
from core.ai.cv_processor import rewrite_cv_for_job
import random
import time
import os
import re
import django
from datetime import datetime

# Initialize Django
django.setup()

# Anti-bot detection measures
HUMAN_LIKE_DELAYS = {
    'min_type': 0.1,  # seconds between keystrokes
    'max_type': 0.3,
    'min_click': 0.5,  # seconds before clicking
    'max_click': 2.0,
    'min_page': 3,     # seconds on page before action
    'max_page': 8
}

def human_delay(action_type):
    """Generate a human-like delay based on action type"""
    if action_type == 'type':
        delay = random.uniform(HUMAN_LIKE_DELAYS['min_type'], HUMAN_LIKE_DELAYS['max_type'])
    elif action_type == 'click':
        delay = random.uniform(HUMAN_LIKE_DELAYS['min_click'], HUMAN_LIKE_DELAYS['max_click'])
    else:  # page load
        delay = random.uniform(HUMAN_LIKE_DELAYS['min_page'], HUMAN_LIKE_DELAYS['max_page'])
    time.sleep(delay)

def solve_captcha(page):
    """Attempt to solve CAPTCHAs with basic techniques"""
    # Simple CAPTCHA solving logic (would need enhancement for production)
    if page.query_selector('img[alt="captcha"]'):
        print("CAPTCHA detected - attempting basic solve...")
        # This is a placeholder - in real implementation use a CAPTCHA solving service
        return False
    return True

def fill_form_field(page, selector, value, field_type='text'):
    """Fill a form field with human-like typing"""
    human_delay('click')
    page.click(selector)
    
    if field_type == 'text':
        for char in value:
            page.type(selector, char, delay=random.uniform(50, 150))
            human_delay('type')
    elif field_type == 'select':
        page.select_option(selector, value=value)
    elif field_type == 'file':
        page.set_input_files(selector, value)

def apply_for_job(job, user):
    """Apply for a single job using Playwright automation"""
    print(f"Applying for: {job.title} at {job.company}")
    
    try:
        with sync_playwright() as p:
            # Launch browser with stealth options
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                viewport={"width": 1366, "height": 768}
            )
            page = context.new_page()
            
            # Navigate to job application page
            page.goto(job.url, timeout=60000)
            human_delay('page')
            
            # Detect and handle CAPTCHA
            if not solve_captcha(page):
                print("CAPTCHA solution failed, skipping application")
                return False, "CAPTCHA solution failed"
            
            # Extract form fields (simplified - would be more robust in production)
            form_selectors = {
                'name': ['#name', '#full-name', '#applicant_name'],
                'email': ['#email', '#applicant_email'],
                'phone': ['#phone', '#telephone'],
                'resume': ['#resume', '#cv', '#file'],
                'cover_letter': ['#cover_letter', '#message', '#description']
            }
            
            # Find actual selectors on page
            actual_selectors = {}
            for field, options in form_selectors.items():
                for option in options:
                    if page.query_selector(option):
                        actual_selectors[field] = option
                        break
            
            # Fill basic information
            if 'name' in actual_selectors:
                fill_form_field(page, actual_selectors['name'], user.full_name)
            
            if 'email' in actual_selectors:
                fill_form_field(page, actual_selectors['email'], user.email)
            
            if 'phone' in actual_selectors and user.phone:
                fill_form_field(page, actual_selectors['phone'], user.phone)
            
            # Upload resume if available
            if 'resume' in actual_selectors and user.optimized_cv_path:
                optimized_cv = rewrite_cv_for_job(user.cv_text, job.description)
                cv_path = save_optimized_cv(optimized_cv, user)
                fill_form_field(page, actual_selectors['resume'], cv_path, 'file')
            
            # Generate and fill cover letter
            if 'cover_letter' in actual_selectors:
                cover_letter = generate_cover_letter(job.description, user.cv_text)
                fill_form_field(page, actual_selectors['cover_letter'], cover_letter)
            
            # Submit application
            human_delay('click')
            page.click('button[type="submit"]')
            
            # Verify submission
            human_delay('page')
            success = False
            if "thank you" in page.content().lower() or "success" in page.content().lower():
                success = True
                print("Application submitted successfully")
            else:
                print("Application submission verification failed")
                
            # Take screenshot for debugging
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"logs/application_{job.id}_{timestamp}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            page.screenshot(path=screenshot_path)
            
            browser.close()
            return success, screenshot_path
            
    except Exception as e:
        print(f"Application failed: {str(e)}")
        return False, str(e)

def save_optimized_cv(cv_text, user):
    """Save optimized CV to file (simplified implementation)"""
    # In a real implementation, this would generate a PDF/DOCX file
    # For demo purposes, we'll create a text file
    cv_path = f"media/cvs/{user.id}_optimized_{int(time.time())}.txt"
    os.makedirs(os.path.dirname(cv_path), exist_ok=True)
    with open(cv_path, 'w') as f:
        f.write(cv_text)
    return cv_path

def process_applications():
    """Process job applications for active users"""
    active_users = UserProfile.objects.filter(job_search_active=True)
    if not active_users:
        print("No active users found")
        return
    
    for user in active_users:
        print(f"Processing applications for: {user.full_name}")
        
        # Get eligible jobs (not applied, not scam, recent)
        eligible_jobs = JobListing.objects.filter(
            applied=False,
            is_scam=False,
            posted_at__gte=datetime.now() - timedelta(days=14)
        ).order_by('?')[:user.daily_application_limit]
        
        if not eligible_jobs:
            print("No eligible jobs found")
            continue
            
        print(f"Found {len(eligible_jobs)} eligible jobs to apply for")
        
        for job in eligible_jobs:
            success, result = apply_for_job(job, user)
            
            # Record application
            JobApplication.objects.create(
                user=user,
                job=job,
                status="SUBMITTED" if success else "FAILED",
                cover_letter=result if not success else "",
                retry_count=1 if not success else 0
            )
            
            # Mark job as applied
            job.applied = True
            job.save()
            
            # Anti-spam delay
            delay = random.uniform(30, 120)
            print(f"Waiting {delay:.
