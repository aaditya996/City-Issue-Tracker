from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('issues.urls')), 
    # --- Naya Code ---
    path('accounts/', include('django.contrib.auth.urls')), # Yeh line sabhi login/logout URLs add kar degi
    # --- End Naya Code ---
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)