
from django.contrib import admin
from django.urls import path,include
import core
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('core.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)