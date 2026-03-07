from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from exchange import views as exchange_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exchange.urls')),
    path('login/', exchange_views.CustomLoginView.as_view(), name='login'),
    path('logout/', exchange_views.custom_logout, name='logout'),
    path('quick-login/', exchange_views.quick_login, name='quick_login'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
