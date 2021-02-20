from django.contrib import admin
from django.urls import include, path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('api/v1/', include('pressevents.urls')),
    path('auth/', obtain_auth_token)
]

