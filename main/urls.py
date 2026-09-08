from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),          # Create corresponding view
    path('events/', views.events_view, name='events'),       # Create corresponding view
    path('events/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('resources/', views.resources_view, name='resources'), # Create corresponding view
    path('contact/', views.contact_view, name='contact'),    # Create corresponding view
    path('faq/', views.faq_view, name='faq'),
    path('join/', views.join_view, name='join'),             # Create corresponding view
    path('privacy-policy/', views.privacy_policy_view, name='privacy'),
    path('terms-of-service/', views.terms_of_service_view, name='terms'),
]