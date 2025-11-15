from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Ingredient, RecipeIngredient
from recipes.models import Recipe, Category

class IngredientModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.ingredient = Ingredient.objects.create(
            name="Tomato",
            unit_of_measure="pieces"
        )
    
    def test_ingredient_creation(self):
        """Test ingredient creation with valid data"""
        self.assertEqual(self.ingredient.name, "Tomato")
        self.assertEqual(self.ingredient.unit_of_measure, "pieces")
        self.assertTrue(isinstance(self.ingredient, Ingredient))
    
    def test_ingredient_str_representation(self):
        """Test string representation of ingredient"""
        expected_str = "Tomato (pieces)"
        self.assertEqual(str(self.ingredient), expected_str)
    
    def test_ingredient_default_unit(self):
        """Test default unit of measure"""
        ingredient_default = Ingredient.objects.create(name="Salt")
        self.assertEqual(ingredient_default.unit_of_measure, "grams")
    
    def test_ingredient_unique_name(self):
        """Test that ingredient names must be unique"""
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(
                name="Tomato",  # Same name as setUp
                unit_of_measure="kg"
            )
    
    def test_ingredient_ordering(self):
        """Test ingredient ordering by name"""
        ingredient_apple = Ingredient.objects.create(name="Apple")
        ingredient_banana = Ingredient.objects.create(name="Banana")
        
        ingredients = Ingredient.objects.all()
        self.assertEqual(ingredients[0].name, "Apple")
        self.assertEqual(ingredients[1].name, "Banana")
        self.assertEqual(ingredients[2].name, "Tomato")

class RecipeIngredientModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(name="Italian")
        self.recipe = Recipe.objects.create(
            name="Tomato Sauce",
            description="Simple tomato sauce",
            cooking_time=20,
            servings=4,
            instructions="Cook tomatoes",
            user=self.user,
            category=self.category
        )
        self.ingredient = Ingredient.objects.create(
            name="Tomato",
            unit_of_measure="pieces"
        )
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=4.0
        )
    
    def test_recipe_ingredient_creation(self):
        """Test recipe ingredient creation"""
        self.assertEqual(self.recipe_ingredient.recipe, self.recipe)
        self.assertEqual(self.recipe_ingredient.ingredient, self.ingredient)
        self.assertEqual(self.recipe_ingredient.quantity, 4.0)
        self.assertTrue(isinstance(self.recipe_ingredient, RecipeIngredient))
    
    def test_recipe_ingredient_str_representation(self):
        """Test string representation of recipe ingredient"""
        expected_str = "4.0 pieces of Tomato for Tomato Sauce"
        self.assertEqual(str(self.recipe_ingredient), expected_str)
    
    def test_recipe_ingredient_unique_together(self):
        """Test unique constraint on recipe and ingredient combination"""
        with self.assertRaises(IntegrityError):
            RecipeIngredient.objects.create(
                recipe=self.recipe,
                ingredient=self.ingredient,  # Same combination
                quantity=2.0
            )
    
    def test_recipe_ingredient_verbose_names(self):
        """Test verbose names"""
        self.assertEqual(str(RecipeIngredient._meta.verbose_name), "Recipe Ingredient")
        self.assertEqual(str(RecipeIngredient._meta.verbose_name_plural), "Recipe Ingredients")
    
    def test_multiple_ingredients_same_recipe(self):
        """Test adding multiple ingredients to same recipe"""
        ingredient2 = Ingredient.objects.create(name="Salt", unit_of_measure="grams")
        recipe_ingredient2 = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=ingredient2,
            quantity=1.0
        )
        
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=self.recipe)
        self.assertEqual(recipe_ingredients.count(), 2)
