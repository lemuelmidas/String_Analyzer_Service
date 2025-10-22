from django.db import models
from django.utils import timezone

class AnalyzedString(models.Model):
    sha256_hash = models.CharField(max_length=64, primary_key=True)
    value = models.TextField()
    properties = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.value[:30]