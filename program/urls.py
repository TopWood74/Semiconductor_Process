from django.urls import path
from . import views

urlpatterns = [
    path('', views.scanimage, name='scanimage'),    
    path('scanimage_upload/', views.scanimage_upload, name='scanimage_upload'),        
]