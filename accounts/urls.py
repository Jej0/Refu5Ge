from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('register/', views.register, name='register'),
    path('verify/<uuid:token>/', views.verif_email, name='verif_email'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('users/', views.user_list, name='user_list'),
    path('profile/<int:user_id>/', views.public_profile, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='login/password_change.html',
        success_url='/accounts/profile/edit/' 
    ), name='password_change')
]