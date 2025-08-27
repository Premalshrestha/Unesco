# App-level urls.py keeps routes modular, reusable, and avoids clutter in the main urls.py.

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.quiz_home, name='home'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
    path('history/', views.quiz_history, name='quiz_history'),

    
     path('upload-document/', views.upload_document, name='upload_document'),
    path('view-health-data/', views.view_health_data, name='view_health_data'),
    path('health-data-json/', views.health_data_json, name='health_data_json'),


   

]
