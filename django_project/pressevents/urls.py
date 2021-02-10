from django.urls import path

from .views import PressEventList, PressEventDetail

urlpatterns = [
    path('<int:pk>/', PressEventDetail.as_view()),
    path('', PressEventList.as_view())
]
