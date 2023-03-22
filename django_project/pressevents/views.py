from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import PressEvent
from .serializers import PressEventSerializer, UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User


class PressEventViewSet(viewsets.ModelViewSet):
    queryset = PressEvent.objects.all()
    serializer_class = PressEventSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
