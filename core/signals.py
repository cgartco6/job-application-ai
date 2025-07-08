from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import JobApplication

@receiver(post_save, sender=JobApplication)
def check_job_offer(sender, instance, **kwargs):
    if instance.status == "OFFER_RECEIVED":
        # Deactivate user's job search
        user = instance.user
        user.job_search_active = False
        user.save()
        
        # Cancel pending applications
        JobApplication.objects.filter(
            user=user, 
            status="PENDING"
        ).update(status="CANCELLED")
