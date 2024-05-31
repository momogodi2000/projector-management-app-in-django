from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import manage_projectors, add_projector, edit_projector, delete_projector
from .views import manage_withdrawals, manage_deposits

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('manage_users/', views.manage_users, name='manage_users'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('manage_projectors/', manage_projectors, name='manage_projectors'),
    path('add_projector/', add_projector, name='add_projector'),
    path('edit_projector/<int:pk>/', edit_projector, name='edit_projector'),
    path('delete_projector/<int:pk>/', delete_projector, name='delete_projector'),

    path('manage_withdrawals/', manage_withdrawals, name='manage_withdrawals'),
    path('manage_deposits/', manage_deposits, name='manage_deposits'),
    path('about_aics/', views.about_aics, name='about_aics'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
