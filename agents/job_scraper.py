import scrapy
from scrapy.crawler import CrawlerProcess
from core.models import JobListing
from core.ai.scam_detector import detect_scam

class SASpider(scrapy.Spider):
    name = "sajobs"
    provinces = ["gauteng", "western-cape", "kwaZulu-natal"]
    
    def start_requests(self):
        urls = [
            f"https://www.careers24.com/jobs/{province}" for province in self.provinces
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for job in response.css('.job-card'):
            title = job.css('.job-title::text').get()
            company = job.css('.job-company::text').get()
            location = job.css('.job-location::text').get()
            description = job.css('.job-desc::text').get()
            
            is_scam, reason = detect_scam(description)
            
            if not is_scam:
                JobListing.objects.update_or_create(
                    title=title,
                    company=company,
                    defaults={
                        'location': location,
                        'description': description,
                        'url': response.urljoin(job.css('a::attr(href)').get()),
                        'source': 'Careers24'
                    }
                )

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0',
        'LOG_LEVEL': 'INFO',
        'ROBOTSTXT_OBEY': False
    })
    process.crawl(SASpider)
    process.start()
