from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    cv_text = models.TextField(blank=True)
    optimized_cv_path = models.CharField(max_length=255, blank=True)
    job_search_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class JobListing(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    source = models.CharField(max_length=100)
    is_scam = models.BooleanField(default=False)
    scam_reason = models.TextField(blank=True)
    province = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, default='South Africa')
    posted_at = models.DateTimeField(auto_now_add=True)
    applied = models.BooleanField(default=False)

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUBMITTED', 'Submitted'),
        ('FAILED', 'Failed'),
        ('OFFER_RECEIVED', 'Offer Received'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField()
    retry_count = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
