from django.urls import path
from .views import RecipeListView, RecipeSearchView

urlpatterns = [
    path('recipes', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/search', RecipeSearchView.as_view(), name='recipe-search'),
]
