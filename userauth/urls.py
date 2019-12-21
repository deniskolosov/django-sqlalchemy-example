from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.user_auth, name='user-auth'),
]
