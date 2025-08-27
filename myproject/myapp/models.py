# models.py
from django.db import models
from django.contrib.auth.models import User
import random

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
        """Get random questions for quiz"""
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
    
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_data')
    
    # Pregnancy Data (25 fields)
    pregnancy_week = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(42)])
    due_date = models.DateField(null=True, blank=True)
    pregnancy_type = models.CharField(max_length=50, null=True, blank=True)  # Single, Twin, etc.
    fetal_heart_rate = models.FloatField(null=True, blank=True)
    fetal_weight = models.FloatField(null=True, blank=True)  # in grams
    fetal_length = models.FloatField(null=True, blank=True)  # in cm
    amniotic_fluid_level = models.CharField(max_length=50, null=True, blank=True)
    placenta_position = models.CharField(max_length=100, null=True, blank=True)
    cervix_length = models.FloatField(null=True, blank=True)  # in mm
    uterine_contractions = models.CharField(max_length=100, null=True, blank=True)
    morning_sickness = models.BooleanField(null=True, blank=True)
    prenatal_vitamins = models.BooleanField(null=True, blank=True)
    dietary_restrictions = models.TextField(null=True, blank=True)
    exercise_routine = models.TextField(null=True, blank=True)
    sleep_quality = models.CharField(max_length=50, null=True, blank=True)
    complications = models.TextField(null=True, blank=True)
    previous_pregnancies = models.IntegerField(null=True, blank=True, default=0)
    miscarriages = models.IntegerField(null=True, blank=True, default=0)
    c_sections = models.IntegerField(null=True, blank=True, default=0)
    vaginal_deliveries = models.IntegerField(null=True, blank=True, default=0)
    gestational_diabetes = models.BooleanField(null=True, blank=True)
    preeclampsia_history = models.BooleanField(null=True, blank=True)
    last_menstrual_period = models.DateField(null=True, blank=True)
    conception_date = models.DateField(null=True, blank=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    
    # Health Data (25 fields)
    systolic_pressure = models.IntegerField(null=True, blank=True)
    diastolic_pressure = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    body_temperature = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)  # in kg
    height = models.FloatField(null=True, blank=True)  # in cm
    bmi = models.FloatField(null=True, blank=True)
    blood_sugar_fasting = models.IntegerField(null=True, blank=True)
    blood_sugar_post_meal = models.IntegerField(null=True, blank=True)
    hemoglobin = models.FloatField(null=True, blank=True)
    hematocrit = models.FloatField(null=True, blank=True)
    white_blood_cells = models.FloatField(null=True, blank=True)
    platelets = models.IntegerField(null=True, blank=True)
    cholesterol_total = models.IntegerField(null=True, blank=True)
    cholesterol_hdl = models.IntegerField(null=True, blank=True)
    cholesterol_ldl = models.IntegerField(null=True, blank=True)
    triglycerides = models.IntegerField(null=True, blank=True)
    thyroid_tsh = models.FloatField(null=True, blank=True)
    thyroid_t3 = models.FloatField(null=True, blank=True)
    thyroid_t4 = models.FloatField(null=True, blank=True)
    iron_levels = models.FloatField(null=True, blank=True)
    vitamin_d = models.FloatField(null=True, blank=True)
    vitamin_b12 = models.FloatField(null=True, blank=True)
    folate_levels = models.FloatField(null=True, blank=True)
    protein_urine = models.CharField(max_length=50, null=True, blank=True)
    
    # Stress Data (25 fields)
    stress_level = models.CharField(max_length=50, null=True, blank=True)  # Low, Medium, High
    anxiety_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    depression_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    sleep_hours = models.FloatField(null=True, blank=True)
    sleep_disturbances = models.BooleanField(null=True, blank=True)
    work_stress = models.CharField(max_length=50, null=True, blank=True)
    relationship_stress = models.CharField(max_length=50, null=True, blank=True)
    financial_stress = models.CharField(max_length=50, null=True, blank=True)
    social_support = models.CharField(max_length=50, null=True, blank=True)
    coping_mechanisms = models.TextField(null=True, blank=True)
    meditation_frequency = models.CharField(max_length=50, null=True, blank=True)
    exercise_stress_relief = models.BooleanField(null=True, blank=True)
    therapy_sessions = models.BooleanField(null=True, blank=True)
    medication_anxiety = models.BooleanField(null=True, blank=True)
    medication_depression = models.BooleanField(null=True, blank=True)
    panic_attacks = models.BooleanField(null=True, blank=True)
    mood_swings = models.CharField(max_length=50, null=True, blank=True)
    irritability = models.CharField(max_length=50, null=True, blank=True)
    concentration_issues = models.BooleanField(null=True, blank=True)
    appetite_changes = models.CharField(max_length=50, null=True, blank=True)
    energy_levels = models.CharField(max_length=50, null=True, blank=True)
    social_withdrawal = models.BooleanField(null=True, blank=True)
    cortisol_levels = models.FloatField(null=True, blank=True)
    stress_triggers = models.TextField(null=True, blank=True)
    relaxation_techniques = models.TextField(null=True, blank=True)
    
    # Metadata
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