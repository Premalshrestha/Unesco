

# App-level urls.py keeps routes modular, reusable, and avoids clutter in the main urls.py.
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    

]
