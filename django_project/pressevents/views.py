from rest_framework import generics

from .models import PressEvent
from .serializers import PressEventSerializer


class PressEventList(generics.ListCreateAPIView):
    queryset = PressEvent.objects.all()

    serializer_class = PressEventSerializer


class PressEventDetail(generics.RetrieveUpdateAPIView):
    queryset = PressEvent.objects.all()
    serializer_class = PressEventSerializer
