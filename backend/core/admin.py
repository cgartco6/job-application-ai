from django.contrib import admin
from .models import UserProfile, JobListing, JobApplication

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'job_search_active')
    search_fields = ('user__username', 'full_name', 'email')

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'source', 'is_scam', 'applied')
    list_filter = ('is_scam', 'applied', 'province', 'country')
    search_fields = ('title', 'company', 'description')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('user__full_name', 'job__title')
