from django.core.management.base import BaseCommand
from core.models import JobApplication
from core.tasks import retry_failed_applications

class Command(BaseCommand):
    help = 'Monitor job applications and handle failures'
    
    def handle(self, *args, **options):
        # Retry failed applications
        retry_failed_applications.delay()
        
        # Check for job offers
        offers = JobApplication.objects.filter(status='OFFER_RECEIVED')
        for offer in offers:
            self.stdout.write(f"Job offer detected for {offer.user.full_name}")
            # Trigger stop condition
            offer.user.job_search_active = False
            offer.user.save()
        
        self.stdout.write(self.style.SUCCESS("Job monitoring completed!"))
