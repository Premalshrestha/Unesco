# admin.py
from django.contrib import admin

from django.contrib import admin

from .models import Question, QuizAttempt, UserAnswer, LifestyleQuestion

@admin.register(LifestyleQuestion)


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


from .models import MotherProfile, PregnancyDetails, HealthCheckup, NutritionTracking, MentalHealthTracking, BabyGrowthTracking, BabyHealthRecords

# Register your models here.
admin.site.register(MotherProfile)
admin.site.register(PregnancyDetails)
admin.site.register(HealthCheckup)
admin.site.register(NutritionTracking)
admin.site.register(MentalHealthTracking)
admin.site.register(BabyGrowthTracking)
admin.site.register(BabyHealthRecords)

from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Category, Discussion, Reply, Vote

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'get_discussions_count', 'get_replies_count']
    list_filter = ['user_type']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['get_discussions_count', 'get_replies_count']
    
    def get_discussions_count(self, obj):
        return obj.user.discussions.count()
    get_discussions_count.short_description = 'Discussions'
    
    def get_replies_count(self, obj):
        return obj.user.replies.count()
    get_replies_count.short_description = 'Replies'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_discussions_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['get_discussions_count']
    
    def get_discussions_count(self, obj):
        return obj.discussions.count()
    get_discussions_count.short_description = 'Discussions'

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'priority', 'is_pinned', 
                   'get_replies_count', 'views', 'created_at']
    list_filter = ['status', 'priority', 'category', 'is_pinned', 'created_at']
    search_fields = ['title', 'content', 'author__username', 'tags']
    readonly_fields = ['views', 'get_replies_count', 'created_at', 'updated_at']
    list_editable = ['status', 'is_pinned']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'category', 'content')
        }),
        ('Settings', {
            'fields': ('status', 'priority', 'is_pinned', 'tags')
        }),
        ('Statistics', {
            'fields': ('views', 'get_replies_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_replies_count(self, obj):
        count = obj.replies.count()
        if count > 0:
            return format_html(
                '<a href="/admin/discussions/reply/?discussion__id__exact={}">{}</a>',
                obj.id, count
            )
        return count
    get_replies_count.short_description = 'Replies'

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['get_discussion_title', 'author', 'is_solution', 'is_consultant_reply', 
                   'get_vote_score', 'created_at']
    list_filter = ['is_solution', 'is_consultant_reply', 'created_at']
    search_fields = ['content', 'author__username', 'discussion__title']
    readonly_fields = ['get_vote_score', 'created_at', 'updated_at']
    
    def get_discussion_title(self, obj):
        return format_html(
            '<a href="/admin/discussions/discussion/{}/change/">{}</a>',
            obj.discussion.id, obj.discussion.title[:50] + ('...' if len(obj.discussion.title) > 50 else '')
        )
    get_discussion_title.short_description = 'Discussion'
    
    def get_vote_score(self, obj):
        upvotes = obj.votes.filter(vote_type=1).count()
        downvotes = obj.votes.filter(vote_type=-1).count()
        score = upvotes - downvotes
        if score > 0:
            return format_html('<span style="color: green;">+{}</span>', score)
        elif score < 0:
            return format_html('<span style="color: red;">{}</span>', score)
        return score
    get_vote_score.short_description = 'Vote Score'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_reply_discussion', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'reply__discussion__title']
    
    def get_reply_discussion(self, obj):
        return f"{obj.reply.discussion.title[:30]}..."
    get_reply_discussion.short_description = 'Discussion'

