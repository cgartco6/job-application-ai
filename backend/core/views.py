from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, JobListing, JobApplication
from .ai.cv_processor import extract_text_from_cv, extract_skills
from .ai.cover_letter_generator import generate_cover_letter
import json

@login_required
def upload_cv(request):
    if request.method == 'POST' and request.FILES.get('cv'):
        cv_file = request.FILES['cv']
        user_profile = request.user.userprofile
        
        # Process CV
        cv_text = extract_text_from_cv(cv_file)
        user_profile.cv_text = cv_text
        user_profile.set_cv_file(cv_file.read())
        user_profile.save()
        
        return redirect('dashboard')
    
    return render(request, 'upload_cv.html')

@login_required
def job_list(request):
    jobs = JobListing.objects.filter(
        is_scam=False, 
        applied=False
    ).order_by('-posted_at')[:100]
    
    return render(request, 'job_list.html', {'jobs': jobs})

@login_required
def application_list(request):
    applications = JobApplication.objects.filter(
        user=request.user.userprofile
    ).order_by('-applied_at')
    
    return render(request, 'applications.html', {'applications': applications})

@login_required
def user_settings(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name', profile.full_name)
        profile.email = request.POST.get('email', profile.email)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.job_search_active = 'job_search_active' in request.POST
        profile.save()
        return redirect('settings')
    
    return render(request, 'settings.html', {'profile': profile})
