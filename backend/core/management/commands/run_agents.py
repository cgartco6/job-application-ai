from django.core.management.base import BaseCommand
from agents.job_scraper import SASpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):
    help = 'Run the job scraping agent'

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(SASpider)
        process.start()
