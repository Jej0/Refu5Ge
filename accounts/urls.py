from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('verify/<uuid:token>/', views.verif_email, name='verif_email'),
    path('profile/', views.profil, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]