from django.urls import path
from . import views

urlpatterns = [
    path('upload-cv/', views.upload_cv, name='upload_cv'),
    path('jobs/', views.job_list, name='job_list'),
    path('applications/', views.application_list, name='application_list'),
    path('settings/', views.user_settings, name='user_settings'),
]
