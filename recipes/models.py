from django.db import models
from django.contrib.postgres.fields import JSONField


class Recipe(models.Model):
    """
    Recipe model to store recipe information.
    """
    # Basic fields
    cuisine = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    title = models.CharField(max_length=500, db_index=True)
    rating = models.FloatField(db_index=True, null=True, blank=True)
    prep_time = models.IntegerField(null=True, blank=True)
    cook_time = models.IntegerField(null=True, blank=True)
    total_time = models.IntegerField(db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    serves = models.CharField(max_length=100, null=True, blank=True)

    # JSON field for nutrients (using JSONB in PostgreSQL)
    nutrients = models.JSONField(null=True, blank=True)

    # Additional fields from original JSON (not required by spec but useful)
    continent = models.CharField(max_length=255, null=True, blank=True)
    country_state = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    ingredients = models.JSONField(null=True, blank=True)
    instructions = models.JSONField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating', 'title']
        indexes = [
            models.Index(fields=['-rating']),
            models.Index(fields=['cuisine']),
            models.Index(fields=['total_time']),
        ]

    def __str__(self):
        return self.title
