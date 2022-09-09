from django.urls import include, path
from rest_framework import routers
from app import views

urlpatterns = [
    path('edit', views.videoEditor),
    path("",views.home)
]