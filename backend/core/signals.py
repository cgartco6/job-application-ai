from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobApplication

@receiver(post_save, sender=JobApplication)
def check_job_offer(sender, instance, **kwargs):
    if instance.status == "OFFER_RECEIVED":
        user_profile = instance.user
        user_profile.job_search_active = False
        user_profile.save()
        
        # Cancel pending applications
        JobApplication.objects.filter(
            user=user_profile, 
            status="PENDING"
        ).update(status="CANCELLED")
