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
        return cls.objects.order_by("?")[:count]

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

class LifestyleQuestion(models.Model):
    question_text= models.CharField(max_length=255)
    correct_answer= models.CharField(max_length=255)
    option_a= models.CharField(max_length=255, blank=True)
    option_b= models.CharField(max_length=255, blank=True)
    option_c= models.CharField(max_length=255, blank=True)
    option_d= models.CharField(max_length=255, blank=True)
    explanation=models.CharField(blank=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text[:50]+ "......."
    
    @classmethod
    def lifestyle_random_question(cls, count=10):
        return cls.objects.order_by("?")[:count]
    

# models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class UserProfile(models.Model):
    """Extend User model to add role information"""
    USER_TYPES = [
        ('user', 'Regular User'),
        ('consultant', 'Consultant'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"

class Category(models.Model):
    """Categories for organizing discussions"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Discussion(models.Model):
    """Main discussion post"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('solved', 'Solved'),
    ]
    
  
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='discussions')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    views = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('discussion_detail', kwargs={'pk': self.pk})
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def reply_count(self):
        """Get total number of replies"""
        return self.replies.count()
    
    def latest_reply(self):
        """Get the latest reply"""
        return self.replies.order_by('-created_at').first()

class Reply(models.Model):
    """Replies to discussions"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_replies')
    is_solution = models.BooleanField(default=False)
    is_consultant_reply = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Reply to {self.discussion.title} by {self.author.username}"
    
    def save(self, *args, **kwargs):
        # Automatically set is_consultant_reply based on user type
        if hasattr(self.author, 'userprofile'):
            self.is_consultant_reply = self.author.userprofile.user_type == 'consultant'
        super().save(*args, **kwargs)

class Vote(models.Model):
    """Voting system for replies"""
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.IntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'reply']
    
    def __str__(self):
        return f"{self.user.username} {'upvoted' if self.vote_type == 1 else 'downvoted'} {self.reply}"


