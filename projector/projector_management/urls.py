from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('projectors/', include('projectors.urls')),
    path('dashboard/', include('dashboard.urls')),
    # Other URL patterns...
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
