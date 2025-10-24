from django.contrib import admin
from .models import AnalyzedString

@admin.register(AnalyzedString)
class AnalyzedStringAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'length',
        'is_palindrome',
        'unique_characters',
        'word_count',
        'sha256_hash',
    )
    search_fields = ('text',)
    list_filter = ('is_palindrome',)
