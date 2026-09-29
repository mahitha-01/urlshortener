from django.db import models

# Create your models here.
class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length = 10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
