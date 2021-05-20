from django.urls import path
from .views import UserRegister, EditProfile, PasswordChange, ProfilePage, UserDelete
from django.contrib.auth import views as auth_views


# app_name = 'account'

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('edit-profile/', EditProfile, name='edit_profile'),
    path('<str:pk>/profile/', ProfilePage.as_view(), name='profile_page'),
    path('user_delete/<int:pk>/', UserDelete.as_view(), name='user_delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password/', PasswordChange.as_view(), name='change_password'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
