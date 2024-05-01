from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('log_out/', views.log_out, name='log_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit'),
    path('process_attendance/', views.process_attendance, name='process_attendance'),  # URL pattern for the attendance processing view
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    # path('capture_attendance/', views.capture_attendance, name='capture_attendance'),
    # Add other URL patterns as needed
]
