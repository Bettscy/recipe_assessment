from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'cuisine', 'rating', 'total_time', 'serves', 'created_at')
    list_filter = ('cuisine', 'rating')
    search_fields = ('title', 'cuisine', 'description')
    ordering = ('-rating', 'title')
    readonly_fields = ('created_at', 'updated_at')
