from django.urls import include, path

from .views import UserViewSet, PressEventViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('press_events', PressEventViewSet, basename='press_events')
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
