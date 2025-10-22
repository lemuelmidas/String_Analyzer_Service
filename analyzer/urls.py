from django.urls import path
from .views import StringListCreateView, StringDetailView, NaturalLanguageFilterView

urlpatterns = [
    path("", StringListCreateView.as_view()),  # GET (list), POST (create)
    path("filter-by-natural-language", NaturalLanguageFilterView.as_view()),
    path("<path:string_value>", StringDetailView.as_view()),  # GET/DELETE
]