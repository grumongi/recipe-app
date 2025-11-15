from django.contrib import admin
from .models import Ingredient, RecipeIngredient

# Register your models here.

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measure')
    search_fields = ('name',)
    list_filter = ('unit_of_measure',)

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'get_quantity_display')
    list_filter = ('ingredient', 'recipe')
    search_fields = ('recipe__name', 'ingredient__name')
    
    def get_quantity_display(self, obj):
        """Display quantity with unit or 'No quantity specified'"""
        if obj.quantity:
            return f"{obj.quantity} {obj.ingredient.unit_of_measure}"
        return "No quantity specified"
    get_quantity_display.short_description = "Quantity"
