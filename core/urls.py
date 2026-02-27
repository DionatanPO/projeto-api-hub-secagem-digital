from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/check-status/', views.check_server_status, name='check_status'),
    path('api/processes/', views.get_processes, name='get_processes'),
    path('api/logs/', views.get_logs, name='get_logs'),
    path('api/network/', views.get_network, name='get_network'),
    path('api/domains/', views.get_domains, name='get_domains'),
    path('api/manage-service/', views.manage_service_api, name='manage_service'),
]
