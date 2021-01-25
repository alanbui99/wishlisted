from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('confirm/', views.confirm, name='confirm'),
    path('unsubscribe/<uuid:item_id>/', views.unsubscribe, name='unsubscribe'),
    path('tracking-error/', views.tracking_error, name='tracking-error'),

]