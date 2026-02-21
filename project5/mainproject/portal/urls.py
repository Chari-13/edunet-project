from django.urls import path
from . import views

urlpatterns = [

    # Basic Pages
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('alerts/', views.alerts, name='alerts'),
    path('safety/', views.safety, name='safety'),
    path('contact/', views.contact, name='contact'),  # fixed typo

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # AI Chat
    path('ai-chat/', views.ai_chat, name='ai_chat'),

    # ✅ Location + Weather API with API key
    path('get-location-weather/', views.get_location_weather, name='get_location_weather'),
    path('disaster-ai/', views.disaster_ai, name='disaster_ai'),

]
