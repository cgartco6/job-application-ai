from celery import shared_task
from .models import JobListing, JobApplication
from .ai.scam_detector import detect_scam
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

@shared_task
def scrape_jobs_task():
    """Task to scrape job listings from various sources"""
    # South African job boards
    sa_job_boards = [
        "https://www.careers24.com/jobs/",
        "https://www.pnet.co.za/jobs/",
        "https://www.careerjunction.co.za/jobs/",
        "https://www.indeed.co.za/jobs"
    ]
    
    for url in sa_job_boards:
        scrape_job_board(url, "South Africa")

@shared_task
def process_applications_task():
    """Process job applications for active users"""
    from .ai.cover_letter_generator import generate_cover_letter
    from .ai.cv_processor import rewrite_cv_for_job
    
    active_users = UserProfile.objects.filter(job_search_active=True)
    
    for user in active_users:
        # Get relevant jobs (max 100 per day)
        jobs = JobListing.objects.filter(
            applied=False, 
            is_scam=False,
            posted_at__gte=datetime.now()-timedelta(days=7)
        ).order_by('?')[:100]
        
        for job in jobs:
            # Optimize CV for this job
            optimized_cv = rewrite_cv_for_job(user.cv_text, job.description)
            
            # Generate cover letter
            cover_letter = generate_cover_letter(job.description, user.id)
            
            # Submit application (simulated)
            application = JobApplication.objects.create(
                user=user,
                job=job,
                status="SUBMITTED",
                cover_letter=cover_letter
            )
            
            # Mark job as applied
            job.applied = True
            job.save()

@shared_task
def retry_failed_applications():
    """Retry failed job applications (max 3 attempts)"""
    failed_apps = JobApplication.objects.filter(
        status="FAILED", 
        retry_count__lt=3
    )
    
    for app in failed_apps:
        # Add retry logic here
        app.retry_count += 1
        app.status = "PENDING"
        app.save()

def scrape_job_board(url, country):
    """Scrape job listings from a specific board"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Job board specific parsing (example for Careers24)
        if "careers24" in url:
            jobs = soup.select('.job-card')
            for job in jobs:
                title = job.select_one('.job-title').text.strip()
                company = job.select_one('.job-company').text.strip()
                location = job.select_one('.job-location').text.strip()
                description = job.select_one('.job-desc').text.strip()
                job_url = job.select_one('a')['href']
                
                is_scam, reason = detect_scam(description)
                
                JobListing.objects.update_or_create(
                    url=job_url,
                    defaults={
                        'title': title,
                        'company': company,
                        'location': location,
                        'description': description,
                        'source': "Careers24",
                        'country': country,
                        'is_scam': is_scam,
                        'scam_reason': reason
                    }
                )
        
        # Add parsing logic for other job boards
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
