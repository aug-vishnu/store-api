
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path,include
from core_api import urls as core_urls
from auth_api import urls as auth_urls

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('core/', include(core_urls)),

    path('admin/', admin.site.urls),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# For the Image View outside API