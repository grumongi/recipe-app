from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
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
    description = models.TextField(blank=True, null=True, help_text="Brief description of the recipe")
    instructions = models.TextField(blank=True, null=True, help_text="Step-by-step cooking instructions")
    cooking_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.PositiveIntegerField(default=1, help_text="Number of servings")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True, help_text="Auto-calculated based on cooking time and ingredients")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
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
    
    def calculate_difficulty(self):
        """Calculate recipe difficulty based on cooking time and number of ingredients"""
        ingredient_count = self.ingredients.count()
        
        # Base difficulty on cooking time and ingredient complexity
        if self.cooking_time < 30 and ingredient_count <= 5:
            return 'Easy'
        elif self.cooking_time <= 60 and ingredient_count <= 10:
            return 'Medium'
        else:
            return 'Hard'
    
    def save(self, *args, **kwargs):
        # Auto-calculate difficulty if not manually set
        if not self.difficulty:
            # Need to save first to get access to ingredients if this is a new recipe
            super().save(*args, **kwargs)
            self.difficulty = self.calculate_difficulty()
            super().save(update_fields=['difficulty'])
        else:
            super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_date']
