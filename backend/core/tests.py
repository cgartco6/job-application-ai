from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, JobListing, JobApplication
from .ai.scam_detector import detect_scam

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass',
            email='test@example.com'
        )
        self.profile = UserProfile.objects.get(user=self.user)
        
    def test_user_profile_creation(self):
        self.assertEqual(self.profile.email, 'test@example.com')
        self.assertTrue(self.profile.job_search_active)
        
    def test_job_listing_creation(self):
        job = JobListing.objects.create(
            title='Software Developer',
            company='Tech Company',
            location='Cape Town',
            description='Develop software applications',
            url='http://example.com/job/1',
            source='Test'
        )
        self.assertEqual(job.country, 'South Africa')
        
    def test_scam_detection(self):
        # Test scam detection
        scam_desc = "Pay R500 registration fee to start working from home today!"
        is_scam, reason = detect_scam(scam_desc)
        self.assertTrue(is_scam)
        self.assertIn("registration fee", reason)
        
        # Test legitimate job
        legit_desc = "Seeking qualified software engineer with 5+ years experience"
        is_scam, reason = detect_scam(legit_desc)
        self.assertFalse(is_scam)
