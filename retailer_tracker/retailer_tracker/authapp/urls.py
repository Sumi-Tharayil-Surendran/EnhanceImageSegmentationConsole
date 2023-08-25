from django.contrib import admin
from django.urls import include, path
from authapp.views import login
from authapp.views import register
from authapp.views import logout,activate,activation_sent_view,password_reset_sent_view,password_reset_activate
from authapp.views import forgot_password

urlpatterns = [
    path("", include("mainapp.urls")),
    path("register", register, name="register"),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    #path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    # path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('sent/', activation_sent_view, name="activation_sent"),

    path('forgot-password', forgot_password, name='forgot_password'), 
    path('password_reset/<uidb64>/<token>/', password_reset_activate, name='password_reset_activate'),
    path('password_reset_sent/', password_reset_sent_view, name="password_reset_sent"),
    
]
