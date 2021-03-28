from django.contrib import admin
from django.urls import include, path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('pressevents.urls')),
    path('auth/', obtain_auth_token),
    path('', include('store.urls', namespace='store')),
    path('store/cart/', include('cart.urls', namespace='cart'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
