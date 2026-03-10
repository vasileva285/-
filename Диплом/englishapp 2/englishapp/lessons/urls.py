from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='lessons/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('lesson/<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<slug:lesson_slug>/exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('api/exercise/<int:exercise_id>/submit/', views.submit_exercise, name='submit_exercise'),
    path('progress/', views.progress_view, name='progress'),
    path('settings/', views.profile_settings, name='profile_settings'),
]

