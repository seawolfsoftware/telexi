
from django.urls import path

from . import views


urlpatterns = [
    # path('', views.subscribe, name='subscribe'),
    path('subscribers', views.subscribers, name='subscribers'),
    path('confirm/', views.confirm, name='confirmed'),
]