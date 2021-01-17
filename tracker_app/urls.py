from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('confirm/', views.confirm, name='confirm'),
    path('tracking_error/', views.tracking_error, name='tracking_error'),

]