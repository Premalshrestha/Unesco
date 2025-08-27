from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import random

# ==========================
# Quiz Models
# ==========================

class Question(models.Model):
    question_text = models.TextField()
    correct_answer = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question_text[:50] + "..."
    
    @classmethod
    def get_random_questions(cls, count=10):
        questions = list(cls.objects.all())
        if len(questions) >= count:
            return random.sample(questions, count)
        return questions

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=50, null=True, blank=True)  # For anonymous users
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    score_percentage = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        user_identifier = self.user.username if self.user else f"Anonymous ({self.session_key})"
        return f"{user_identifier} - {self.score_percentage}% ({self.completed_at})"

class UserAnswer(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    
    def __str__(self):
        return f"Q{self.question.id} - {'Correct' if self.is_correct else 'Wrong'}"

# ==========================
# Mother & Health Models
# ==========================

class MotherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mother_profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    blood_type = models.CharField(max_length=3)
    height = models.FloatField()
    weight = models.FloatField()
    medical_history = models.TextField()
    allergies = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    image = models.ImageField(upload_to='uploads/mother/')
    
    def __str__(self):
        return self.user.username

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_data')
    
    # Pregnancy Data (partial example; add more fields as needed)
    pregnancy_week = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(42)])
    due_date = models.DateField(null=True, blank=True)
    pregnancy_type = models.CharField(max_length=50, null=True, blank=True)
    fetal_heart_rate = models.FloatField(null=True, blank=True)
    fetal_weight = models.FloatField(null=True, blank=True)
    
    # Health Data (partial example; add more fields as needed)
    systolic_pressure = models.IntegerField(null=True, blank=True)
    diastolic_pressure = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Health data for {self.user.username}"

class UploadedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_docs')
    document = models.FileField(upload_to='health_documents/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    extracted_data = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.original_filename} - {self.user.username}"

# ==========================
# Placeholder Models
# ==========================
# Fill in details later
class PregnancyDetails(models.Model):
    pass

class HealthCheckup(models.Model):
    pass

class NutritionTracking(models.Model):
    pass

class MentalHealthTracking(models.Model):
    pass

class BabyGrowthTracking(models.Model):
    pass

class BabyHealthRecords(models.Model):
    pass
