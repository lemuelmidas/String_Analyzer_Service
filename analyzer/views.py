from rest_framework import generics
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer

class StringListCreateView(generics.ListCreateAPIView):
    queryset = AnalyzedString.objects.all()
    serializer_class = AnalyzedStringSerializer