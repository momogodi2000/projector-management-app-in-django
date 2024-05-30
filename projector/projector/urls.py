"""
URL configuration for projector project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from projector_management import views
from .views import manage_projectors, add_projector, edit_projector, delete_projector
from django.conf.urls.static import static




urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage_projectors/', manage_projectors, name='manage_projectors'),
    path('add_projector/', add_projector, name='add_projector'),
    path('edit_projector/<int:pk>/', edit_projector, name='edit_projector'),
    path('delete_projector/<int:pk>/', delete_projector, name='delete_projector'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


