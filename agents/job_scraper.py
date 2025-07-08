import scrapy
from core.models import JobListing
from django.utils import timezone
from core.ai.scam_detector import detect_scam

class SASpider(scrapy.Spider):
    name = "sajobs"
    provinces = ["gauteng", "western-cape", "kwaZulu-natal"]
    start_urls = [
        f"https://www.careers24.com/jobs/{province}" for province in provinces
    ]

    def parse(self, response):
        for job in response.css('.job-card'):
            title = job.css('.job-title::text').get()
            company = job.css('.job-company::text').get()
            location = job.css('.job-location::text').get()
            description = job.css('.job-desc::text').get()
            url = job.css('a::attr(href)').get()
            
            is_scam, reason = detect_scam(description)
            
            JobListing.objects.update_or_create(
                url=url,
                defaults={
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description,
                    'is_scam': is_scam,
                    'scam_reason': reason,
                    'source': 'Careers24'
                }
            )
