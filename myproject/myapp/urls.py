
# App-level urls.py keeps routes modular, reusable, and avoids clutter in the main urls.py.

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name='home'),
    path('foodquiz/', views.quiz_home, name='home'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
    path('history/', views.quiz_history, name='quiz_history'),

    
     path('upload-document/', views.upload_document, name='upload_document'),
    path('view-health-data/', views.view_health_data, name='view_health_data'),
    path('health-data-json/', views.health_data_json, name='health_data_json'),
    path('discussion/', views.discussion_list, name='discussion_list'),
    path('create/', views.create_discussion, name='create_discussion'),
    path('<int:pk>/', views.discussion_detail, name='discussion_detail'),
    

    #these are for the discussion page
    # Category pages
    path('category/<slug:slug>/', views.category_discussions, name='category_discussions'),
    
    # User-specific pages
    path('discussions/', views.my_discussions, name='my_discussions'),
    
    
    # AJAX endpoints
    path('<int:discussion_pk>/reply/', views.add_reply, name='add_reply'),
    
    

]
