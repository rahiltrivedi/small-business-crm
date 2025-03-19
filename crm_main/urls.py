"""
URL configuration for crm_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""crm_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path, reverse_lazy, include  # Added include

from django.contrib.auth.views import LogoutView
from apps.common.views import HomeView, SignUpView, DashboardView, ProfileUpdateView, ProfileView, FrontView

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', FrontView.as_view(), name='front'),
    
    path('home/', HomeView.as_view(), name='home'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Authentication 
    path('register/', SignUpView.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'
        ), name='login'
    ),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('change_password', auth_views.PasswordChangeView.as_view(
        template_name='common/change_password.html', success_url='/'), name='change_password'),

    # Password Reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password_reset.html',
             subject_template_name='common/password-reset/password_reset_subject.txt',
             email_template_name='common/password-reset/password_reset_email.html',
             success_url=reverse_lazy('password_reset_done')
         ), name='password_reset'),
    
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password_reset_done.html'
         ), name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password_reset_confirm.html'
         ), name='password_reset_confirm'),
    
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password_reset_complete.html'
         ), name='password_reset_complete'),

    path('oauth/', include('social_django.urls', namespace='social')),  # Social Auth
    path('account/', include('allauth.urls')),  # Allauth URLs for login, registration, etc.

    # Include the URLs for Clients, Leads, Invoices
    path("common/", include("apps.common.urls")),
]

# Serve media files in debug mode
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




