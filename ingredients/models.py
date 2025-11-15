from django.db import models

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit_of_measure = models.CharField(max_length=50, default='grams')
    
    def __str__(self):
        return f"{self.name} ({self.unit_of_measure})"
    
    class Meta:
        ordering = ['name']

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(null=True, blank=True, help_text="Optional quantity")
    
    def __str__(self):
        if self.quantity:
            return f"{self.quantity} {self.ingredient.unit_of_measure} of {self.ingredient.name} for {self.recipe.name}"
        else:
            return f"{self.ingredient.name} for {self.recipe.name}"
    
    class Meta:
        unique_together = ('recipe', 'ingredient')
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe Ingredients"
