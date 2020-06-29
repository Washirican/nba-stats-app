from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='shotcharts-home'),
    path('about/', views.about, name='shotcharts-about'),
]
