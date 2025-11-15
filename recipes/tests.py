from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Category, Recipe

class CategoryModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name="Italian",
            description="Traditional Italian cuisine"
        )
    
    def test_category_creation(self):
        """Test category creation with valid data"""
        self.assertEqual(self.category.name, "Italian")
        self.assertEqual(self.category.description, "Traditional Italian cuisine")
        self.assertTrue(isinstance(self.category, Category))
    
    def test_category_str_representation(self):
        """Test string representation of category"""
        self.assertEqual(str(self.category), "Italian")
    
    def test_category_verbose_name_plural(self):
        """Test the verbose name plural"""
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")

class RecipeModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name="Italian",
            description="Traditional Italian cuisine"
        )
        self.recipe = Recipe.objects.create(
            name="Spaghetti Carbonara",
            description="Classic Italian pasta dish",
            cooking_time=30,
            difficulty="Medium",
            servings=4,
            instructions="Cook pasta, mix with eggs and cheese",
            user=self.user,
            category=self.category
        )
    
    def test_recipe_creation(self):
        """Test recipe creation with valid data"""
        self.assertEqual(self.recipe.name, "Spaghetti Carbonara")
        self.assertEqual(self.recipe.description, "Classic Italian pasta dish")
        self.assertEqual(self.recipe.cooking_time, 30)
        self.assertEqual(self.recipe.difficulty, "Medium")
        self.assertEqual(self.recipe.servings, 4)
        self.assertEqual(self.recipe.user, self.user)
        self.assertEqual(self.recipe.category, self.category)
        self.assertTrue(isinstance(self.recipe, Recipe))
    
    def test_recipe_str_representation(self):
        """Test string representation of recipe"""
        self.assertEqual(str(self.recipe), "Spaghetti Carbonara")
    
    def test_recipe_default_difficulty(self):
        """Test default difficulty level"""
        recipe_no_difficulty = Recipe.objects.create(
            name="Test Recipe",
            description="Test description",
            cooking_time=15,
            servings=2,
            instructions="Test instructions",
            user=self.user
        )
        self.assertEqual(recipe_no_difficulty.difficulty, "Easy")
    
    def test_recipe_difficulty_choices(self):
        """Test difficulty choices validation"""
        valid_difficulties = ['Easy', 'Medium', 'Hard']
        for difficulty in valid_difficulties:
            recipe = Recipe.objects.create(
                name=f"Test Recipe {difficulty}",
                description="Test description",
                cooking_time=15,
                difficulty=difficulty,
                servings=2,
                instructions="Test instructions",
                user=self.user
            )
            self.assertEqual(recipe.difficulty, difficulty)
    
    def test_recipe_ordering(self):
        """Test recipe ordering by created_date"""
        # Create another recipe
        recipe2 = Recipe.objects.create(
            name="Pizza Margherita",
            description="Classic pizza",
            cooking_time=25,
            servings=2,
            instructions="Make dough, add toppings, bake",
            user=self.user,
            category=self.category
        )
        
        # Check ordering (newest first)
        recipes = Recipe.objects.all()
        self.assertEqual(recipes[0], recipe2)  # Most recent first
        self.assertEqual(recipes[1], self.recipe)
    
    def test_recipe_timestamps(self):
        """Test automatic timestamp creation"""
        self.assertIsNotNone(self.recipe.created_date)
        self.assertIsNotNone(self.recipe.updated_date)
    
    def test_recipe_without_category(self):
        """Test recipe creation without category"""
        recipe_no_category = Recipe.objects.create(
            name="Simple Recipe",
            description="No category recipe",
            cooking_time=10,
            servings=1,
            instructions="Simple instructions",
            user=self.user
        )
        self.assertIsNone(recipe_no_category.category)
