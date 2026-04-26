from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/rooms/', views.search_rooms, name='search_rooms'),
    path('search/devices/', views.search_devices, name='search_devices'),
    path('search/attributes/', views.search_attributes, name='search_attributes'),
]