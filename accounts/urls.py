from django.urls import path
from django.contrib.auth.decorators import login_required
from accounts import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', login_required(views.ProfileView.profile), name='profile')
]
