
# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from .models import Question, QuizAttempt, UserAnswer
import json
import random

def quiz_home(request):
    """Home page for the quiz"""
    total_questions = Question.objects.count()
    context = {
        'total_questions': total_questions,
        'quiz_questions': min(10, total_questions)
    }
    return render(request, 'home.html', context)

def start_quiz(request):
    """Start a new quiz with random questions"""
    questions = Question.get_random_questions(10)
    
    # Store question IDs in session for this quiz attempt
    question_ids = [q.id for q in questions]
    request.session['quiz_questions'] = question_ids
    request.session['current_question'] = 0
    request.session['user_answers'] = {}
    
    context = {
        'questions': questions,
        'total_questions': len(questions)
    }
    return render(request, 'quiz.html', context)

@csrf_exempt
def submit_quiz(request):
    """Handle quiz submission and calculate score"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answers = data.get('answers', {})
            
            # Get questions from session
            question_ids = request.session.get('quiz_questions', [])
            questions = Question.objects.filter(id__in=question_ids)
            
            correct_count = 0
            total_questions = len(questions)
            
            # Create quiz attempt
            quiz_attempt = QuizAttempt.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                total_questions=total_questions,
                correct_answers=0,  # Will update this
                score_percentage=0  # Will update this
            )
            
            # Process each answer
            for question in questions:
                question_id = str(question.id)
                selected_answer = answers.get(question_id, '')
                is_correct = selected_answer == question.correct_answer
                
                if is_correct:
                    correct_count += 1
                
                # Save user answer
                UserAnswer.objects.create(
                    quiz_attempt=quiz_attempt,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=is_correct
                )
            
            # Update quiz attempt with final score
            score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
            quiz_attempt.correct_answers = correct_count
            quiz_attempt.score_percentage = score_percentage
            quiz_attempt.save()
            
            # Clear session data
            request.session.pop('quiz_questions', None)
            request.session.pop('current_question', None)
            request.session.pop('user_answers', None)
            
            return JsonResponse({
                'success': True,
                'score': correct_count,
                'total': total_questions,
                'percentage': round(score_percentage, 2),
                'quiz_id': quiz_attempt.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def quiz_results(request, quiz_id):
    """Show detailed quiz results"""
    try:
        quiz_attempt = QuizAttempt.objects.get(id=quiz_id)
        
        # Check if user can view this result
        if request.user.is_authenticated:
            if quiz_attempt.user != request.user:
                return redirect('quiz_home')
        else:
            if quiz_attempt.session_key != request.session.session_key:
                return redirect('quiz_home')
        
        # Get detailed answers
        user_answers = UserAnswer.objects.filter(quiz_attempt=quiz_attempt).select_related('question')
        
        context = {
            'quiz_attempt': quiz_attempt,
            'user_answers': user_answers,
        }
        return render(request, 'results.html', context)
        
    except QuizAttempt.DoesNotExist:
        return redirect('quiz_home')

def quiz_history(request):
   
    
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-completed_at')[:20]
    
    context = {
        'attempts': attempts
    }
    return render(request, 'history.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import PyPDF2
import re
import json
from datetime import datetime, date
from .models import UserData, UploadedDocument
from .forms import DocumentUploadForm

class HealthDataExtractor:
    """Extract health-related data from PDF text"""
    
    def __init__(self):
        # Define patterns for different types of data
        self.pregnancy_patterns = {
            'pregnancy_week': r'(?:pregnancy week|gestational week|week)\s*:?\s*(\d+)',
            'due_date': r'(?:due date|delivery date|EDD)\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'fetal_heart_rate': r'(?:fetal heart rate|FHR)\s*:?\s*(\d+\.?\d*)',
            'fetal_weight': r'(?:fetal weight|estimated fetal weight)\s*:?\s*(\d+\.?\d*)',
            'morning_sickness': r'(?:morning sickness|nausea)\s*:?\s*(yes|no|present|absent)',
            'gestational_diabetes': r'(?:gestational diabetes|GDM)\s*:?\s*(yes|no|positive|negative)',
            'preeclampsia_history': r'(?:preeclampsia|pre-eclampsia)\s*:?\s*(yes|no|history|present)',
        }
        
        self.health_patterns = {
            'systolic_pressure': r'(?:systolic|blood pressure)\s*:?\s*(\d+)(?:/\d+)?',
            'diastolic_pressure': r'(?:diastolic|\d+/)\s*(\d+)',
            'heart_rate': r'(?:heart rate|pulse|HR)\s*:?\s*(\d+)',
            'body_temperature': r'(?:temperature|temp)\s*:?\s*(\d+\.?\d*)',
            'weight': r'(?:weight|wt)\s*:?\s*(\d+\.?\d*)\s*(?:kg|lbs)?',
            'height': r'(?:height|ht)\s*:?\s*(\d+\.?\d*)\s*(?:cm|ft|in)?',
            'blood_sugar_fasting': r'(?:fasting glucose|FBS|fasting blood sugar)\s*:?\s*(\d+)',
            'hemoglobin': r'(?:hemoglobin|Hb|HGB)\s*:?\s*(\d+\.?\d*)',
        }
        
        self.stress_patterns = {
            'stress_level': r'(?:stress level|stress)\s*:?\s*(low|medium|high|mild|moderate|severe)',
            'anxiety_score': r'(?:anxiety score|anxiety level)\s*:?\s*(\d+)',
            'depression_score': r'(?:depression score|depression level)\s*:?\s*(\d+)',
            'sleep_hours': r'(?:sleep hours|hours of sleep)\s*:?\s*(\d+\.?\d*)',
            'sleep_disturbances': r'(?:sleep disturbances|sleep problems)\s*:?\s*(yes|no|present|absent)',
        }
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.lower()  # Convert to lowercase for easier matching
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_data(self, text):
        """Extract all types of data from text"""
        extracted_data = {'pregnancy': {}, 'health': {}, 'stress': {}}
        
        # Extract pregnancy data
        for field, pattern in self.pregnancy_patterns.items():
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches:
                value = matches.group(1)
                if field in ['morning_sickness', 'gestational_diabetes', 'preeclampsia_history']:
                    extracted_data['pregnancy'][field] = value.lower() in ['yes', 'positive', 'present']
                else:
                    extracted_data['pregnancy'][field] = value
        
        # Extract health data
        for field, pattern in self.health_patterns.items():
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches:
                extracted_data['health'][field] = matches.group(1)
        
        # Extract stress data
        for field, pattern in self.stress_patterns.items():
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches:
                value = matches.group(1)
                if field == 'sleep_disturbances':
                    extracted_data['stress'][field] = value.lower() in ['yes', 'present']
                else:
                    extracted_data['stress'][field] = value
        
        return extracted_data

@login_required
def upload_document(request):
    """Handle document upload and data extraction"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded document
            document = form.save(commit=False)
            document.user = request.user
            document.original_filename = request.FILES['document'].name
            document.save()
            
            # Extract data from PDF
            extractor = HealthDataExtractor()
            pdf_text = extractor.extract_text_from_pdf(document.document.file)
            extracted_data = extractor.extract_data(pdf_text)
            
            # Save extracted data to document record
            document.extracted_data = extracted_data
            document.processed = True
            document.save()
            
            # Update or create UserData
            user_data, created = UserData.objects.get_or_create(user=request.user)
            
            # Update pregnancy data
            for field, value in extracted_data['pregnancy'].items():
                if value:  # Only update if value exists
                    setattr(user_data, field, value)
            
            # Update health data
            for field, value in extracted_data['health'].items():
                if value:  # Only update if value exists
                    try:
                        # Convert to appropriate type
                        if field in ['systolic_pressure', 'diastolic_pressure', 'heart_rate', 
                                   'blood_sugar_fasting', 'platelets', 'cholesterol_total', 
                                   'cholesterol_hdl', 'cholesterol_ldl', 'triglycerides']:
                            value = int(float(value))
                        elif field in ['body_temperature', 'weight', 'height', 'bmi', 
                                     'hemoglobin', 'hematocrit', 'white_blood_cells']:
                            value = float(value)
                        setattr(user_data, field, value)
                    except (ValueError, TypeError):
                        pass  # Skip invalid values
            
            # Update stress data
            for field, value in extracted_data['stress'].items():
                if value:  # Only update if value exists
                    try:
                        if field in ['anxiety_score', 'depression_score']:
                            value = int(float(value))
                        elif field == 'sleep_hours':
                            value = float(value)
                        setattr(user_data, field, value)
                    except (ValueError, TypeError):
                        pass  # Skip invalid values
            
            user_data.save()
            
            messages.success(request, 'Document uploaded and processed successfully!')
            return redirect('upload_document')
    else:
        form = DocumentUploadForm()
    
    # Get recent uploads for display
    recent_uploads = UploadedDocument.objects.filter(user=request.user).order_by('-upload_date')[:5]
    
    return render(request, 'upload_document.html', {
        'form': form,
        'recent_uploads': recent_uploads
    })

@login_required
def view_health_data(request):
    """Display user's health data"""
    try:
        user_data = UserData.objects.get(user=request.user)
    except UserData.DoesNotExist:
        user_data = None
    
    uploaded_docs = UploadedDocument.objects.filter(user=request.user).order_by('-upload_date')
    
    return render(request, 'view_health_data.html', {
        'user_data': user_data,
        'uploaded_docs': uploaded_docs
    })

@login_required
def health_data_json(request):
    """Return health data as JSON for AJAX requests"""
    try:
        user_data = UserData.objects.get(user=request.user)
        
        # Convert model instance to dictionary
        data = {}
        for field in user_data._meta.fields:
            if field.name not in ['id', 'user']:
                value = getattr(user_data, field.name)
                if isinstance(value, date):
                    value = value.isoformat()
                data[field.name] = value
        
        return JsonResponse({
            'success': True,
            'data': data
        })
    except UserData.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No health data found'
        })



#this is for discussion page
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count, Prefetch
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import Discussion, Reply, Category, Vote, Bookmark, UserProfile
from .forms import DiscussionForm, ReplyForm

def discussion_list(request):
    """Main discussion list with search and filtering"""
    discussions = Discussion.objects.select_related('author', 'category').annotate(
        reply_count=Count('replies')
    )
    
    # Search functionality
    query = request.GET.get('q', '')
    if query:
        discussions = discussions.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        )
    
    # Category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        discussions = discussions.filter(category__slug=category_slug)
    
    # Status filtering
    status = request.GET.get('status')
    if status:
        discussions = discussions.filter(status=status)
    
    # Priority filtering
    priority = request.GET.get('priority')
    if priority:
        discussions = discussions.filter(priority=priority)
    
    # User type filtering (consultant posts, user posts)
    user_type = request.GET.get('user_type')
    if user_type:
        user_profiles = UserProfile.objects.filter(user_type=user_type)
        user_ids = user_profiles.values_list('user_id', flat=True)
        discussions = discussions.filter(author_id__in=user_ids)
    
    # Sorting
    sort_by = request.GET.get('sort', 'latest')
    if sort_by == 'popular':
        discussions = discussions.order_by('-views', '-created_at')
    elif sort_by == 'replies':
        discussions = discussions.order_by('-reply_count', '-created_at')
    else:  # latest
        discussions = discussions.order_by('-is_pinned', '-created_at')
    
    # Pagination
    paginator = Paginator(discussions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'current_category': category_slug,
        'current_status': status,
        'current_priority': priority,
        'current_user_type': user_type,
        'current_sort': sort_by,
    }
    
    return render(request, 'discussion_list.html', context)

def discussion_detail(request, pk):
    """Individual discussion page with replies"""
    discussion = get_object_or_404(
        Discussion.objects.select_related('author', 'category'),
        pk=pk
    )
    
    # Increment view count
    discussion.views += 1
    discussion.save(update_fields=['views'])
    
    # Get replies with nested structure
    replies = Reply.objects.filter(discussion=discussion).select_related(
        'author', 'author__userprofile'
    ).prefetch_related(
        'votes',
        Prefetch('child_replies', queryset=Reply.objects.select_related('author'))
    ).annotate(
        vote_score=Count('votes__vote_type', filter=Q(votes__vote_type=1)) - 
                   Count('votes__vote_type', filter=Q(votes__vote_type=-1))
    )
    
    # Separate parent replies (not nested under other replies)
    parent_replies = replies.filter(parent_reply=None).order_by('-is_solution', 'created_at')
    
    # Check if user has bookmarked this discussion
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(
            user=request.user, 
            discussion=discussion
        ).exists()
    
    # Reply form
    reply_form = ReplyForm()
    
    context = {
        'discussion': discussion,
        'replies': parent_replies,
        'reply_form': reply_form,
        'is_bookmarked': is_bookmarked,
    }
    
    return render(request, 'discussion_detail.html', context)

@login_required
def create_discussion(request):
    """Create a new discussion"""
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            messages.success(request, 'Discussion created successfully!')
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm()
    
    return render(request, 'create_discussion.html', {'form': form})

@login_required
@require_POST
def add_reply(request, discussion_pk):
    """Add a reply to a discussion"""
    discussion = get_object_or_404(Discussion, pk=discussion_pk)
    form = ReplyForm(request.POST)
    
    if form.is_valid():
        reply = form.save(commit=False)
        reply.discussion = discussion
        reply.author = request.user
        
        # Handle nested replies
        parent_id = request.POST.get('parent_id')
        if parent_id:
            parent_reply = get_object_or_404(Reply, pk=parent_id)
            reply.parent_reply = parent_reply
        
        reply.save()
        messages.success(request, 'Reply added successfully!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('discussion_detail', pk=discussion_pk)

@login_required
@require_POST
def vote_reply(request, reply_pk):
    """Vote on a reply (AJAX endpoint)"""
    reply = get_object_or_404(Reply, pk=reply_pk)
    vote_type = int(request.POST.get('vote_type'))  # 1 for upvote, -1 for downvote
    
    if vote_type not in [1, -1]:
        return JsonResponse({'error': 'Invalid vote type'}, status=400)
    
    # Get or create vote
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        reply=reply,
        defaults={'vote_type': vote_type}
    )
    
    if not created:
        if vote.vote_type == vote_type:
            # Remove vote if clicking the same vote type
            vote.delete()
            action = 'removed'
        else:
            # Change vote type
            vote.vote_type = vote_type
            vote.save()
            action = 'changed'
    else:
        action = 'added'
    
    # Calculate new vote score
    vote_score = reply.votes.filter(vote_type=1).count() - reply.votes.filter(vote_type=-1).count()
    
    return JsonResponse({
        'success': True,
        'action': action,
        'vote_score': vote_score,
        'vote_type': vote_type if action != 'removed' else None
    })

@login_required
@require_POST
def mark_as_solution(request, reply_pk):
    """Mark a reply as solution (only discussion author or consultants can do this)"""
    reply = get_object_or_404(Reply, pk=reply_pk)
    discussion = reply.discussion
    
    # Check permissions
    is_author = discussion.author == request.user
    is_consultant = (hasattr(request.user, 'userprofile') and 
                    request.user.userprofile.user_type == 'consultant')
    
    if not (is_author or is_consultant):
        return HttpResponseForbidden("You don't have permission to mark solutions.")
    
    # Toggle solution status
    reply.is_solution = not reply.is_solution
    reply.save()
    
    # Update discussion status if marked as solution
    if reply.is_solution:
        discussion.status = 'solved'
        discussion.save()
        messages.success(request, 'Reply marked as solution!')
    else:
        # Check if there are other solutions, if not, mark as open
        if not discussion.replies.filter(is_solution=True).exists():
            discussion.status = 'open'
            discussion.save()
        messages.success(request, 'Solution mark removed!')
    
    return redirect('discussion_detail', pk=discussion.pk)

@login_required
@require_POST
def toggle_bookmark(request, discussion_pk):
    """Bookmark/unbookmark a discussion"""
    discussion = get_object_or_404(Discussion, pk=discussion_pk)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        discussion=discussion
    )
    
    if not created:
        bookmark.delete()
        bookmarked = False
        message = 'Bookmark removed!'
    else:
        bookmarked = True
        message = 'Discussion bookmarked!'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'bookmarked': bookmarked,
            'message': message
        })
    else:
        messages.success(request, message)
        return redirect('discussion_detail', pk=discussion_pk)

@login_required
def my_discussions(request):
    """User's own discussions"""
    discussions = Discussion.objects.filter(author=request.user).annotate(
        reply_count=Count('replies')
    ).order_by('-created_at')
    
    paginator = Paginator(discussions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'my_discussions.html', {'page_obj': page_obj})

@login_required
def bookmarked_discussions(request):
    """User's bookmarked discussions"""
    bookmarks = Bookmark.objects.filter(user=request.user).select_related(
        'discussion', 'discussion__author', 'discussion__category'
    ).annotate(
        reply_count=Count('discussion__replies')
    ).order_by('-created_at')
    
    paginator = Paginator(bookmarks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookmarked_discussions.html', {'page_obj': page_obj})

def category_discussions(request, slug):
    """Discussions in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    discussions = Discussion.objects.filter(category=category).select_related(
        'author', 'category'
    ).annotate(
        reply_count=Count('replies')
    ).order_by('-is_pinned', '-created_at')
    
    paginator = Paginator(discussions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'category_discussions.html', context)