from django.contrib import admin
from .models import Recipe, Category
from ingredients.models import RecipeIngredient

# Register your models here.

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3  # Show 3 empty ingredient forms by default
    verbose_name = "Ingredient"
    verbose_name_plural = "Ingredients"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty', 'cooking_time', 'user', 'created_date', 'get_ingredients_display')
    list_filter = ('difficulty', 'category', 'created_date')
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')
    inlines = [RecipeIngredientInline]
    
    def get_ingredients_display(self, obj):
        """Display ingredients in the list view"""
        ingredients = obj.get_ingredients_list()
        if ingredients:
            return "; ".join(ingredients[:3])  # Show first 3 ingredients
        return "No ingredients"
    get_ingredients_display.short_description = "Ingredients" # type: ignore
