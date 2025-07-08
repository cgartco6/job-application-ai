import scrapy
from scrapy.crawler import CrawlerProcess
from core.models import JobListing
from core.ai.scam_detector import detect_scam
import datetime

class SASpider(scrapy.Spider):
    name = "sajobs"
    allowed_domains = ["careers24.com", "pnet.co.za", "indeed.co.za"]
    
    def start_requests(self):
        provinces = ['gauteng', 'western-cape', 'kwaZulu-natal', 'eastern-cape', 
                    'free-state', 'limpopo', 'mpumalanga', 'north-west', 'northern-cape']
        
        for province in provinces:
            yield scrapy.Request(
                url=f"https://www.careers24.com/jobs/{province}",
                meta={'province': province}
            )
            
        # International job sites
        yield scrapy.Request("https://www.indeed.com/worldwide-jobs")

    def parse(self, response):
        province = response.meta.get('province', 'international')
        
        for job in response.css('.job-card'):
            title = job.css('.job-title::text').get()
            company = job.css('.job-company::text').get()
            location = job.css('.job-location::text').get()
            description = job.css('.job-desc::text').get()
            url = response.urljoin(job.css('a::attr(href)').get())
            
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
                    'source': response.url,
                    'province': province,
                    'country': 'South Africa' if province != 'international' else 'International'
                }
            )

def scrape_jobs():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_LEVEL': 'INFO',
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 2,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'jobs.json'
    })
    
    process.crawl(SASpider)
    process.start()
