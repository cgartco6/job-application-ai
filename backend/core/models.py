from django.db import models
from django.contrib.auth.models import User

class JobListing(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    source = models.CharField(max_length=100)
    is_scam = models.BooleanField(default=False)
    scam_reason = models.TextField(blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    applied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cv_text = models.TextField(blank=True, null=True)
    optimized_cv_path = models.CharField(max_length=255, blank=True, null=True)
    job_search_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

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
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CH
