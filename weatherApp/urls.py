from django.urls import path

from weatherApp import views

urlpatterns = [
    path('', views.weather_view, name='weather_view')
]
