from django.urls import path
from . import views

urlpatterns = [
    path('admin_home', views.home_view, name='admin_home'),
    path('admin_analysis', views.analysis_view, name='admin_analysis'),

    path('admin_dataManagement', views.data_management_view,
         name='admin_dataManagement'),
    path('admin_reports', views.report_view, name='admin_reports'),
    path('admin_settings', views.settings_view, name='admin_settings'),
    path('admin_support', views.support_view, name='admin_support'),
    path('admin_activityLog', views.activityLog_view, name='admin_activityLog'),

]
