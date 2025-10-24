from django.db import models

class AnalyzedString(models.Model):
    text = models.TextField()
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=64)
    character_frequency_map = models.JSONField()

    def __str__(self):
        return self.text[:50]
