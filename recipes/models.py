from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=200)
    cooking_time = models.IntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Easy')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    ingredients = models.ManyToManyField('ingredients.Ingredient', through='ingredients.RecipeIngredient', blank=True)
    
    def __str__(self):
        return self.name
    
    def get_ingredients_list(self):
        """Return a formatted list of ingredients with optional quantities"""
        recipe_ingredients = self.recipeingredient_set.all() # type: ignore
        result = []
        for ri in recipe_ingredients:
            if ri.quantity:
                result.append(f"{ri.quantity} {ri.ingredient.unit_of_measure} of {ri.ingredient.name}")
            else:
                result.append(f"{ri.ingredient.name}")
        return result
    
    class Meta:
        ordering = ['-created_date']
