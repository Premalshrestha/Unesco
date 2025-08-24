from django.urls import path
from . import views

urlpatterns =[
    path('',views.homepage,name='homepage'),
    path('mrs/',views.msr,name='msr')
]