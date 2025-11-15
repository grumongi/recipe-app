from django.shortcuts import render
from .models import Recipe

# Create your views here.

def recipe_list(request):
    """Display all recipes with their ingredients"""
    recipes = Recipe.objects.all().select_related('category', 'user').prefetch_related('recipeingredient_set__ingredient')
    return render(request, 'recipes/list.html', {'recipes': recipes})
