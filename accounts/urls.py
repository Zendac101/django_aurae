from django.urls import path
from . import views

urlpatterns = [
    path('registerUser', views.LogRes, name='registerUser'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
