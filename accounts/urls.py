from django.urls import path
from . import views

urlpatterns = [
    path('', views.LogRes, name='registerUser'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm,
         name='password_reset_confirm'),
]
