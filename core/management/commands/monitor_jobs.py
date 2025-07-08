from django.core.management.base import BaseCommand
from core.models import JobApplication

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Check failed applications
        failed = JobApplication.objects.filter(status="FAILED")
        
        for app in failed:
            if app.retry_count < 3:
                self.stdout.write(f"Retrying application {app.id}")
                # Re-run application logic
                app.retry_count += 1
                app.save()
