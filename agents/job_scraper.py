import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse
from core.models import JobListing
from core.ai.scam_detector import detect_scam
import random
import time

# South African job boards with province-specific URLs
SA_JOB_BOARDS = {
    "Careers24": {
        "base_url": "https://www.careers24.com/jobs/{province}/",
        "provinces": [
            "eastern-cape", "free-state", "gauteng", 
            "kwaZulu-natal", "limpopo", "mpumalanga", 
            "north-west", "northern-cape", "western-cape"
        ]
    },
    "PNet": {
        "base_url": "https://www.pnet.co.za/jobs/{province}",
        "provinces": [
            "eastern-cape", "free-state", "gauteng",
            "kwazulu-natal", "limpopo", "mpumalanga",
            "north-west", "northern-cape", "western-cape"
        ]
    },
    "Indeed": {
        "base_url": "https://za.indeed.com/jobs?q=&l={province}",
        "provinces": [
            "Eastern+Cape", "Free+State", "Gauteng",
            "KwaZulu-Natal", "Limpopo", "Mpumalanga",
            "North+West", "Northern+Cape", "Western+Cape"
        ]
    }
}

# International job boards
INTERNATIONAL_JOB_BOARDS = [
    "https://www.linkedin.com/jobs/",
    "https://www.indeed.com/worldwide",
    "https://www.glassdoor.com/Job/index.htm"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_job_board(url, source, country="South Africa", province=None):
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Careers24 parsing
        if "careers24" in url:
            for job in soup.select('.job-card'):
                title = job.select_one('.job-title').get_text(strip=True) if job.select_one('.job-title') else "No Title"
                company = job.select_one('.job-company').get_text(strip=True) if job.select_one('.job-company') else "Unknown Company"
                location = job.select_one('.job-location').get_text(strip=True) if job.select_one('.job-location') else "Location Not Specified"
                description = job.select_one('.job-desc').get_text(strip=True) if job.select_one('.job-desc') else "No Description"
                job_url = job.select_one('a')['href'] if job.select_one('a') else "#"
                
                # Make sure URL is absolute
                if not job_url.startswith('http'):
                    job_url = f"https://www.careers24.com{job_url}"
                
                save_job_listing(title, company, location, description, job_url, source, country, province)
        
        # PNet parsing
        elif "pnet" in url:
            for job in soup.select('.job-element'):
                title = job.select_one('.job-title').get_text(strip=True) if job.select_one('.job-title') else "No Title"
                company = job.select_one('.company-name').get_text(strip=True) if job.select_one('.company-name') else "Unknown Company"
                location = job.select_one('.job-location').get_text(strip=True) if job.select_one('.job-location') else "Location Not Specified"
                description = job.select_one('.job-description').get_text(strip=True) if job.select_one('.job-description') else "No Description"
                job_url = job.select_one('a')['href'] if job.select_one('a') else "#"
                
                save_job_listing(title, company, location, description, job_url, source, country, province)
        
        # Indeed parsing
        elif "indeed" in url:
            for job in soup.select('.jobsearch-SerpJobCard'):
                title_elem = job.select_one('.jobtitle a')
                title = title_elem.get_text(strip=True) if title_elem else "No Title"
                company = job.select_one('.company').get_text(strip=True) if job.select_one('.company') else "Unknown Company"
                location = job.select_one('.location').get_text(strip=True) if job.select_one('.location') else "Location Not Specified"
                description = job.select_one('.summary').get_text(strip=True) if job.select_one('.summary') else "No Description"
                job_url = f"https://za.indeed.com{title_elem['href']}" if title_elem else "#"
                
                save_job_listing(title, company, location, description, job_url, source, country, province)
        
        # Add parsing logic for other job boards as needed
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")

def save_job_listing(title, company, location, description, url, source, country, province):
    # Detect scam
    is_scam, scam_reason = detect_scam(description)
    
    # Skip scam jobs
    if is_scam:
        print(f"Skipping potential scam: {title} at {company} - Reason: {scam_reason}")
        return
    
    # Create or update job listing
    JobListing.objects.update_or_create(
        url=url,
        defaults={
            'title': title,
            'company': company,
            'location': location,
            'description': description,
            'source': source,
            'country': country,
            'province': province,
            'is_scam': is_scam,
            'scam_reason': scam_reason
        }
    )

def scrape_south_african_jobs():
    """Scrape job listings from South African job boards by province"""
    for source, config in SA_JOB_BOARDS.items():
        for province in config["provinces"]:
            url = config["base_url"].format(province=province)
            print(f"Scraping {source} in {province.replace('+', ' ')}...")
            scrape_job_board(url, source, "South Africa", province)
            # Random delay to avoid being blocked
            time.sleep(random.uniform(2, 5))

def scrape_international_jobs():
    """Scrape job listings from international job boards"""
    for url in INTERNATIONAL_JOB_BOARDS:
        print(f"Scraping international jobs from {url}...")
        scrape_job_board(url, urlparse(url).netloc, "International")
        # Random delay to avoid being blocked
        time.sleep(random.uniform(3, 7))

def run_scraping():
    """Main function to run all scraping tasks"""
    print("Starting South African job scraping...")
    scrape_south_african_jobs()
    
    print("Starting international job scraping...")
    scrape_international_jobs()
    
    print("Job scraping completed successfully!")

if __name__ == "__main__":
    import django
    django.setup()
    run_scraping()
