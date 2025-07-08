from transformers import pipeline
from core.models import UserProfile

def generate_cover_letter(job_description, user_id):
    """Generate personalized cover letter using AI"""
    try:
        user = UserProfile.objects.get(id=user_id)
        
        generator = pipeline('text-generation', model='gpt2')
        
        prompt = f"""
        Job Description: {job_description[:1000]}
        Applicant: {user.full_name}
        Skills: {user.cv_text[:500]}
        
        Write a professional cover letter that matches my skills with the job requirements:
        """
        
        cover_letter = generator(
            prompt,
            max_length=500,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9
        )[0]['generated_text']
        
        return cover_letter.split("Write a professional")[1].strip()
    except Exception as e:
        print(f"Cover letter generation failed: {e}")
        return "Default cover letter text"
