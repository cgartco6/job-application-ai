from django.core.management.base import BaseCommand
from core.tasks import scrape_jobs_task, process_applications_task

class Command(BaseCommand):
    help = 'Run all job application agents'
    
    def handle(self, *args, **options):
        self.stdout.write("Starting job scraping agent...")
        scrape_jobs_task.delay()
        
        self.stdout.write("Starting application submission agent...")
        process_applications_task.delay()
        
        self.stdout.write(self.style.SUCCESS("Agents started successfully!"))
