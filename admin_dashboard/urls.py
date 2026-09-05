from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home_view, name='home'),
    path('analysis', views.analysis_view, name='analysis'),

    path('dataManagement', views.data_management_view, name='dataManagement'),
    path('reports', views.report_view, name='reports'),
    path('settings', views.settings_view, name='settings'),
    path('support', views.support_view, name='support'),
    path('activityLog', views.activityLog_view, name='activityLog'),

]
