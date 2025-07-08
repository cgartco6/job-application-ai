from celery import shared_task
from .models import JobListing
from agents import job_scraper

@shared_task
def scrape_jobs_task():
    # Scrape South African jobs by province
    provinces = ['gauteng', 'western-cape', 'kwaZulu-natal', 'eastern-cape', 
                'free-state', 'limpopo', 'mpumalanga', 'north-west', 'northern-cape']
    
    for province in provinces:
        job_scraper.scrape_province(province)
    
    # Scrape international jobs
    job_scraper.scrape_international()
    
    # Apply scam detection
    job_scraper.detect_scams()

@shared_task
def process_applications_task():
    from agents import application_bot
    application_bot.process_applications()
