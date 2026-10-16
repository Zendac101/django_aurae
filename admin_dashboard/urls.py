from django.urls import path
from . import views

urlpatterns = [
    path('admin_home', views.admin_home_view, name='admin_home'),
    path('admin_analysis', views.admin_analysis_view, name='admin_analysis'),

    path('admin_dataManagement', views.admin_data_management_view,
         name='admin_dataManagement'),
    path('admin_reports', views.admin_report_view, name='admin_reports'),
    path('admin_settings', views.admin_settings_view, name='admin_settings'),
    path('admin_support', views.admin_support_view, name='admin_support'),
    path('admin_activityLog', views.admin_activityLog_view,
         name='admin_activityLog'),

]
