from django.urls import path
from .views import StringListCreateView

urlpatterns = [
    path('strings/', StringListCreateView.as_view(), name='string-list-create'),
]