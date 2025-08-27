# admin.py
from django.contrib import admin
from .models import Question, QuizAttempt, UserAnswer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'correct_answer', 'created_at']
    list_filter = ['created_at']
    search_fields = ['question_text', 'correct_answer']
    
    def question_text_short(self, obj):
        return obj.question_text[:100] + "..." if len(obj.question_text) > 100 else obj.question_text
    question_text_short.short_description = 'Question'

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ['question', 'selected_answer', 'is_correct']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['get_user_display', 'score_percentage', 'correct_answers', 'total_questions', 'completed_at']
    list_filter = ['completed_at', 'score_percentage']
    readonly_fields = ['user', 'session_key', 'total_questions', 'correct_answers', 'score_percentage', 'completed_at']
    inlines = [UserAnswerInline]
    
    def get_user_display(self, obj):
        if obj.user:
            return obj.user.username
        return f"Anonymous ({obj.session_key})"
    get_user_display.short_description = 'User'

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_attempt', 'question_short', 'selected_answer', 'is_correct']
    list_filter = ['is_correct', 'quiz_attempt__completed_at']
    readonly_fields = ['quiz_attempt', 'question', 'selected_answer', 'is_correct']
    
    def question_short(self, obj):
        return obj.question.question_text[:50] + "..." if len(obj.question.question_text) > 50 else obj.question.question_text
    question_short.short_description = 'Question'



#---------------------this is for pdf upload----------------


from django.contrib import admin
from .models import UserData, UploadedDocument

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'pregnancy_week', 'last_updated', 'created_at']
    list_filter = ['last_updated', 'created_at', 'pregnancy_week']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'last_updated']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'created_at', 'last_updated')
        }),
        ('Pregnancy Data', {
            'fields': (
                'pregnancy_week', 'due_date', 'pregnancy_type', 'fetal_heart_rate',
                'fetal_weight', 'fetal_length', 'amniotic_fluid_level', 'placenta_position',
                'cervix_length', 'uterine_contractions', 'morning_sickness', 'prenatal_vitamins',
                'dietary_restrictions', 'exercise_routine', 'sleep_quality', 'complications',
                'previous_pregnancies', 'miscarriages', 'c_sections', 'vaginal_deliveries',
                'gestational_diabetes', 'preeclampsia_history', 'last_menstrual_period',
                'conception_date', 'estimated_delivery_date'
            ),
            'classes': ('collapse',)
        }),
        ('Health Vitals', {
            'fields': (
                'systolic_pressure', 'diastolic_pressure', 'heart_rate', 'body_temperature',
                'weight', 'height', 'bmi', 'blood_sugar_fasting', 'blood_sugar_post_meal',
                'hemoglobin', 'hematocrit', 'white_blood_cells', 'platelets', 'cholesterol_total',
                'cholesterol_hdl', 'cholesterol_ldl', 'triglycerides', 'thyroid_tsh',
                'thyroid_t3', 'thyroid_t4', 'iron_levels', 'vitamin_d', 'vitamin_b12',
                'folate_levels', 'protein_urine'
            ),
            'classes': ('collapse',)
        }),
        ('Stress & Mental Health', {
            'fields': (
                'stress_level', 'anxiety_score', 'depression_score', 'sleep_hours',
                'sleep_disturbances', 'work_stress', 'relationship_stress', 'financial_stress',
                'social_support', 'coping_mechanisms', 'meditation_frequency', 'exercise_stress_relief',
                'therapy_sessions', 'medication_anxiety', 'medication_depression', 'panic_attacks',
                'mood_swings', 'irritability', 'concentration_issues', 'appetite_changes',
                'energy_levels', 'social_withdrawal', 'cortisol_levels', 'stress_triggers',
                'relaxation_techniques'
            ),
            'classes': ('collapse',)
        })
    )

@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'user', 'upload_date', 'processed']
    list_filter = ['processed', 'upload_date']
    search_fields = ['original_filename', 'user__username']
    readonly_fields = ['upload_date']
=======
from .models import MotherProfile, PregnancyDetails, HealthCheckup, NutritionTracking, MentalHealthTracking, BabyGrowthTracking, BabyHealthRecords

# Register your models here.
admin.site.register(MotherProfile)
admin.site.register(PregnancyDetails)
admin.site.register(HealthCheckup)
admin.site.register(NutritionTracking)
admin.site.register(MentalHealthTracking)
admin.site.register(BabyGrowthTracking)
admin.site.register(BabyHealthRecords)
