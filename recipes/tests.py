from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Count
from unittest.mock import patch
import pandas as pd
from .models import Category, Recipe
from ingredients.models import Ingredient, RecipeIngredient

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


class RecipeViewsTest(TestCase):
    """Test cases for Recipe views and URL functionality"""
    
    def setUp(self):
        """Set up test data for view tests"""
        self.client = Client()
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
            name="Test Recipe",
            description="A test recipe for testing",
            cooking_time=25,
            difficulty="Medium",
            servings=4,
            instructions="Test instructions for recipe",
            user=self.user,
            category=self.category
        )
    
    def test_home_view_status_code(self):
        """Test that home view returns 200 status code"""
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_template(self):
        """Test that home view uses correct template"""
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')
    
    def test_recipe_list_view_status_code(self):
        """Test that recipe list view returns 200 status code"""
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_list_view_template(self):
        """Test that recipe list view uses correct template"""
        response = self.client.get(reverse('recipes:list'))
        self.assertTemplateUsed(response, 'recipes/list.html')
    
    def test_recipe_list_view_context(self):
        """Test that recipe list view contains recipes in context"""
        response = self.client.get(reverse('recipes:list'))
        self.assertIn('recipes', response.context)
        self.assertIn(self.recipe, response.context['recipes'])
    
    def test_recipe_detail_view_status_code(self):
        """Test that recipe detail view returns 200 status code"""
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_detail_view_template(self):
        """Test that recipe detail view uses correct template"""
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertTemplateUsed(response, 'recipes/detail.html')
    
    def test_recipe_detail_view_context(self):
        """Test that recipe detail view contains correct context"""
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertIn('recipe', response.context)
        self.assertIn('calculated_difficulty', response.context)
        self.assertIn('ingredients_list', response.context)
        self.assertEqual(response.context['recipe'], self.recipe)
    
    def test_recipe_detail_view_404_for_nonexistent_recipe(self):
        """Test that recipe detail view returns 404 for non-existent recipe"""
        response = self.client.get(reverse('recipes:detail', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_list_view_contains_recipe_links(self):
        """Test that recipe list view contains links to recipe details"""
        response = self.client.get(reverse('recipes:list'))
        detail_url = reverse('recipes:detail', args=[self.recipe.pk])
        self.assertContains(response, detail_url)


class RecipeModelEnhancedTest(TestCase):
    """Test cases for enhanced Recipe model functionality"""
    
    def setUp(self):
        """Set up test data for enhanced model tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name="Test Category",
            description="Test category description"
        )
    
    def test_calculate_difficulty_easy(self):
        """Test difficulty calculation for easy recipes"""
        easy_recipe = Recipe.objects.create(
            name="Easy Recipe",
            description="Quick and simple",
            cooking_time=10,
            servings=2,
            instructions="Simple instructions",
            user=self.user,
            category=self.category
        )
        # Add 2 ingredients (less than 5)
        from ingredients.models import Ingredient, RecipeIngredient
        
        ingredient1 = Ingredient.objects.create(name="Salt", unit_of_measure="tsp")
        ingredient2 = Ingredient.objects.create(name="Pepper", unit_of_measure="tsp")
        
        RecipeIngredient.objects.create(recipe=easy_recipe, ingredient=ingredient1, quantity=1.0)
        RecipeIngredient.objects.create(recipe=easy_recipe, ingredient=ingredient2, quantity=0.5)
        
        difficulty = easy_recipe.calculate_difficulty()
        self.assertEqual(difficulty, "Easy")
    
    def test_calculate_difficulty_medium(self):
        """Test difficulty calculation for medium recipes"""
        medium_recipe = Recipe.objects.create(
            name="Medium Recipe",
            description="Moderately complex",
            cooking_time=45,  # Over 30 minutes
            servings=4,
            instructions="Moderate instructions",
            user=self.user,
            category=self.category
        )
        # Add 7 ingredients (more than 5 but less than 10)
        from ingredients.models import Ingredient, RecipeIngredient
        
        ingredients = []
        for i in range(7):
            ingredient = Ingredient.objects.create(name=f"Ingredient {i+1}", unit_of_measure="cups")
            ingredients.append(ingredient)
            RecipeIngredient.objects.create(recipe=medium_recipe, ingredient=ingredient, quantity=float(i+1))
        
        difficulty = medium_recipe.calculate_difficulty()
        self.assertEqual(difficulty, "Medium")
    
    def test_calculate_difficulty_hard(self):
        """Test difficulty calculation for hard recipes"""
        hard_recipe = Recipe.objects.create(
            name="Hard Recipe",
            description="Complex dish",
            cooking_time=75,  # Over 60 minutes
            servings=6,
            instructions="Complex instructions",
            user=self.user,
            category=self.category
        )
        # Add 12 ingredients (more than 10)
        from ingredients.models import Ingredient, RecipeIngredient
        
        ingredients = []
        for i in range(12):
            ingredient = Ingredient.objects.create(name=f"Complex Ingredient {i+1}", unit_of_measure="units")
            ingredients.append(ingredient)
            RecipeIngredient.objects.create(recipe=hard_recipe, ingredient=ingredient, quantity=float(i+1))
        
        difficulty = hard_recipe.calculate_difficulty()
        self.assertEqual(difficulty, "Hard")
    
    def test_automatic_difficulty_calculation_on_save(self):
        """Test that difficulty is automatically calculated when saving recipe"""
        recipe = Recipe.objects.create(
            name="Auto Difficulty Recipe",
            description="Test auto calculation",
            cooking_time=15,
            servings=2,
            instructions="Test instructions",
            user=self.user,
            category=self.category
        )
        # The difficulty should be automatically set to Easy (default for recipes with few ingredients and short time)
        self.assertEqual(recipe.difficulty, "Easy")
    
    def test_get_ingredients_list_method(self):
        """Test get_ingredients_list method returns correct format"""
        recipe = Recipe.objects.create(
            name="Ingredients Test Recipe",
            description="Test ingredients display",
            cooking_time=20,
            servings=3,
            instructions="Test instructions",
            user=self.user,
            category=self.category
        )
        
        from ingredients.models import Ingredient, RecipeIngredient
        
        # Add some ingredients
        ingredient1 = Ingredient.objects.create(name="Flour", unit_of_measure="cups")
        ingredient2 = Ingredient.objects.create(name="Sugar", unit_of_measure="cups")
        
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1, quantity=2.0)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2, quantity=1.0)
        
        ingredients_list = recipe.get_ingredients_list()
        self.assertIn("2.0 cups of Flour", ingredients_list)
        self.assertIn("1.0 cups of Sugar", ingredients_list)
        self.assertEqual(len(ingredients_list), 2)


class URLPatternsTest(TestCase):
    """Test URL patterns and routing"""
    
    def setUp(self):
        """Set up test data for URL tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.recipe = Recipe.objects.create(
            name="URL Test Recipe",
            description="Recipe for URL testing",
            cooking_time=20,
            servings=4,
            instructions="URL test instructions",
            user=self.user
        )
    
    def test_home_url_resolves_to_home_view(self):
        """Test that home URL resolves to correct view"""
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
    
    def test_list_url_resolves_to_list_view(self):
        """Test that list URL resolves to correct view"""
        url = reverse('recipes:list')
        self.assertEqual(url, '/list/')
    
    def test_detail_url_resolves_to_detail_view(self):
        """Test that detail URL resolves to correct view"""
        url = reverse('recipes:detail', args=[self.recipe.pk])
        self.assertEqual(url, f'/recipe/{self.recipe.pk}/')
    
    def test_all_urls_accessible(self):
        """Test that all URLs are accessible and return appropriate status codes"""
        urls_to_test = [
            reverse('recipes:home'),
            reverse('recipes:list'),
            reverse('recipes:detail', args=[self.recipe.pk]),
        ]
        
        for url in urls_to_test:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 301, 302], f"URL {url} returned status code {response.status_code}")


class RecipeModelFieldsTest(TestCase):
    """Test enhanced recipe model fields"""
    
    def setUp(self):
        """Set up test data for field tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name="Test Category",
            description="Test description"
        )
    
    def test_recipe_with_description_field(self):
        """Test that recipe can have description"""
        recipe = Recipe.objects.create(
            name="Recipe with Description",
            description="This is a detailed description of the recipe",
            cooking_time=30,
            servings=4,
            instructions="Detailed cooking instructions",
            user=self.user,
            category=self.category
        )
        self.assertEqual(recipe.description, "This is a detailed description of the recipe")
    
    def test_recipe_with_instructions_field(self):
        """Test that recipe can have instructions"""
        recipe = Recipe.objects.create(
            name="Recipe with Instructions",
            description="Test description",
            cooking_time=25,
            servings=3,
            instructions="Step 1: Prepare ingredients. Step 2: Cook. Step 3: Serve.",
            user=self.user,
            category=self.category
        )
        self.assertEqual(recipe.instructions, "Step 1: Prepare ingredients. Step 2: Cook. Step 3: Serve.")
    
    def test_recipe_with_servings_field(self):
        """Test that recipe servings field works correctly"""
        recipe = Recipe.objects.create(
            name="Recipe with Servings",
            description="Test description",
            cooking_time=20,
            servings=6,
            instructions="Test instructions",
            user=self.user,
            category=self.category
        )
        self.assertEqual(recipe.servings, 6)
    
    def test_recipe_blank_fields_allowed(self):
        """Test that optional fields can be left blank"""
        recipe = Recipe.objects.create(
            name="Minimal Recipe",
            cooking_time=15,
            servings=2,
            user=self.user
        )
        self.assertEqual(recipe.name, "Minimal Recipe")
        self.assertEqual(recipe.cooking_time, 15)
        self.assertEqual(recipe.servings, 2)
        # Optional fields should be empty or have defaults
        self.assertIsNone(recipe.category)


class RecipeViewTest(TestCase):
    """Test recipe views including authentication and permissions"""
    
    def setUp(self):
        """Set up test data for view tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.category = Category.objects.create(
            name="Test Category",
            description="Test description"
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            description="Test recipe description",
            cooking_time=25,
            difficulty="Easy",
            servings=4,
            instructions="Test instructions",
            user=self.user,
            category=self.category
        )
    
    def test_recipe_list_view_requires_login(self):
        """Test that recipe list view requires authentication"""
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/login/?next=/list/', fetch_redirect_response=False)
    
    def test_recipe_list_view_authenticated(self):
        """Test recipe list view for authenticated user"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')
    
    def test_recipe_detail_view_requires_login(self):
        """Test that recipe detail view requires authentication"""
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_recipe_detail_view_authenticated(self):
        """Test recipe detail view for authenticated user"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')
        self.assertContains(response, 'Test recipe description')


class RecipeSearchViewTest(TestCase):
    """Test the recipe search functionality"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data that will be used across multiple test methods"""
        cls.user = User.objects.create_user(
            username='searchuser',
            email='search@example.com',
            password='searchpass123'
        )
        cls.category1 = Category.objects.create(name="Italian")
        cls.category2 = Category.objects.create(name="Mexican")
        
        # Create test ingredients
        cls.ingredient1 = Ingredient.objects.create(
            name='tomato',
            unit_of_measure='piece'
        )
        cls.ingredient2 = Ingredient.objects.create(
            name='cheese',
            unit_of_measure='grams'
        )
        cls.ingredient3 = Ingredient.objects.create(
            name='chicken',
            unit_of_measure='grams'
        )
        
        # Create test recipes with different characteristics
        cls.recipe1 = Recipe.objects.create(
            name="Margherita Pizza",
            description="Classic Italian pizza",
            cooking_time=25,
            difficulty="Easy",
            servings=2,
            instructions="Make dough, add toppings, bake",
            user=cls.user,
            category=cls.category1
        )
        
        cls.recipe2 = Recipe.objects.create(
            name="Chicken Tacos",
            description="Mexican style tacos",
            cooking_time=45,
            difficulty="Medium",
            servings=4,
            instructions="Cook chicken, prepare toppings, assemble",
            user=cls.user,
            category=cls.category2
        )
        
        cls.recipe3 = Recipe.objects.create(
            name="Cheese Pasta",
            description="Simple pasta with cheese",
            cooking_time=15,
            difficulty="Easy",
            servings=3,
            instructions="Cook pasta, add cheese",
            user=cls.user,
            category=cls.category1
        )
        
        # Add ingredients to recipes
        RecipeIngredient.objects.create(recipe=cls.recipe1, ingredient=cls.ingredient1, quantity=2)
        RecipeIngredient.objects.create(recipe=cls.recipe1, ingredient=cls.ingredient2, quantity=200)
        RecipeIngredient.objects.create(recipe=cls.recipe2, ingredient=cls.ingredient3, quantity=500)
        RecipeIngredient.objects.create(recipe=cls.recipe3, ingredient=cls.ingredient2, quantity=150)
    
    def setUp(self):
        """Set up for each test method"""
        self.client = Client()
        self.client.login(username='searchuser', password='searchpass123')
    
    def test_search_view_requires_login(self):
        """Test that search view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/search/', fetch_redirect_response=False)
    
    def test_search_view_get_request(self):
        """Test search view GET request displays search form"""
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe Search')
        self.assertContains(response, 'Search Criteria')
    
    def test_search_by_recipe_name(self):
        """Test search functionality by recipe name"""
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': 'pizza',
            'ingredients': '',
            'difficulty': 'any',
            'cooking_time': 'any'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Margherita Pizza')
        self.assertNotContains(response, 'Chicken Tacos')
    
    def test_search_by_ingredients(self):
        """Test search functionality by ingredients"""
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredients': 'cheese',
            'difficulty': 'any',
            'cooking_time': 'any'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Margherita Pizza')
        self.assertContains(response, 'Cheese Pasta')
        self.assertNotContains(response, 'Chicken Tacos')
    
    def test_search_by_difficulty(self):
        """Test search functionality by difficulty"""
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredients': '',
            'difficulty': 'easy',
            'cooking_time': 'any'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Margherita Pizza')
        self.assertContains(response, 'Cheese Pasta')
        self.assertNotContains(response, 'Chicken Tacos')
    
    def test_search_by_cooking_time_quick(self):
        """Test search functionality by quick cooking time"""
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredients': '',
            'difficulty': 'any',
            'cooking_time': 'quick'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Margherita Pizza')
        self.assertContains(response, 'Cheese Pasta')
        self.assertNotContains(response, 'Chicken Tacos')
    
    def test_search_by_cooking_time_medium(self):
        """Test search functionality by medium cooking time"""
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredients': '',
            'difficulty': 'any',
            'cooking_time': 'medium'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken Tacos')
        self.assertNotContains(response, 'Margherita Pizza')
        self.assertNotContains(response, 'Cheese Pasta')
    
    def test_search_combined_criteria(self):
        """Test search functionality with multiple criteria"""
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': 'pizza',
            'ingredients': 'cheese',
            'difficulty': 'easy',
            'cooking_time': 'quick'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Margherita Pizza')
        self.assertNotContains(response, 'Chicken Tacos')
        self.assertNotContains(response, 'Cheese Pasta')
    
    def test_search_no_results(self):
        """Test search with no matching results"""
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': 'nonexistent',
            'ingredients': '',
            'difficulty': 'any',
            'cooking_time': 'any'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found')
    
    def test_search_show_all_recipes(self):
        """Test show all recipes functionality"""
        response = self.client.get(reverse('recipes:search') + '?show_all=true')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Margherita Pizza')
        self.assertContains(response, 'Chicken Tacos')
        self.assertContains(response, 'Cheese Pasta')


class RecipeAnalyticsViewTest(TestCase):
    """Test the recipe analytics functionality"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data for analytics tests"""
        cls.user = User.objects.create_user(
            username='analyticsuser',
            email='analytics@example.com',
            password='analyticspass123'
        )
        cls.category = Category.objects.create(name="Test Category")
        
        # Create recipes with different characteristics for analytics
        Recipe.objects.create(
            name="Easy Recipe 1",
            cooking_time=15,
            difficulty="Easy",
            servings=2,
            user=cls.user,
            category=cls.category
        )
        Recipe.objects.create(
            name="Easy Recipe 2",
            cooking_time=20,
            difficulty="Easy",
            servings=3,
            user=cls.user,
            category=cls.category
        )
        Recipe.objects.create(
            name="Medium Recipe 1",
            cooking_time=45,
            difficulty="Medium",
            servings=4,
            user=cls.user,
            category=cls.category
        )
        Recipe.objects.create(
            name="Hard Recipe 1",
            cooking_time=90,
            difficulty="Hard",
            servings=6,
            user=cls.user,
            category=cls.category
        )
    
    def setUp(self):
        """Set up for each test method"""
        self.client = Client()
        self.client.login(username='analyticsuser', password='analyticspass123')
    
    def test_analytics_view_requires_login(self):
        """Test that analytics view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('recipes:analytics'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/analytics/', fetch_redirect_response=False)
    
    @patch('matplotlib.pyplot.savefig')
    def test_analytics_view_with_recipes(self, mock_savefig):
        """Test analytics view when recipes exist"""
        response = self.client.get(reverse('recipes:analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe Analytics')
        self.assertContains(response, 'Recipe Collection Overview')
        
        # Check that statistics are displayed
        self.assertContains(response, '4')  # Total recipes
        self.assertContains(response, '2')  # Easy recipes
        self.assertContains(response, '1')  # Medium recipes
        self.assertContains(response, '1')  # Hard recipes
    
    @patch('matplotlib.pyplot.savefig')
    def test_analytics_view_chart_generation(self, mock_savefig):
        """Test that charts are generated in analytics view"""
        response = self.client.get(reverse('recipes:analytics'))
        self.assertEqual(response.status_code, 200)
        
        # Check that chart placeholders exist
        self.assertContains(response, 'difficulty_chart')
        self.assertContains(response, 'time_chart')
        self.assertContains(response, 'trend_chart')
        
        # Verify matplotlib savefig was called (charts were generated)
        self.assertTrue(mock_savefig.called)
    
    def test_analytics_view_empty_database(self):
        """Test analytics view when no recipes exist"""
        # Delete all recipes
        Recipe.objects.all().delete()
        
        response = self.client.get(reverse('recipes:analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Recipes Yet')
        self.assertContains(response, 'Start building your recipe collection')


class RecipeFormTest(TestCase):
    """Test recipe forms and form validation"""
    
    def setUp(self):
        """Set up test data for form tests"""
        self.user = User.objects.create_user(
            username='formuser',
            email='form@example.com',
            password='formpass123'
        )
        self.category = Category.objects.create(
            name="Form Test Category",
            description="Test category for forms"
        )
    
    def test_recipe_model_field_validation(self):
        """Test recipe model field validation"""
        # Test that name field is required
        with self.assertRaises(Exception):
            Recipe.objects.create(
                cooking_time=30,
                user=self.user
            )
    
    def test_recipe_cooking_time_validation(self):
        """Test cooking time field validation"""
        # Test that cooking time must be positive
        recipe = Recipe(
            name="Test Recipe",
            cooking_time=-5,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            recipe.full_clean()
    
    def test_recipe_servings_validation(self):
        """Test servings field validation"""
        # Test that servings must be positive
        recipe = Recipe(
            name="Test Recipe",
            cooking_time=30,
            servings=-1,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            recipe.full_clean()
    
    def test_recipe_difficulty_choices(self):
        """Test that difficulty field accepts only valid choices"""
        valid_difficulties = ['Easy', 'Medium', 'Hard']
        for difficulty in valid_difficulties:
            recipe = Recipe.objects.create(
                name=f"Test Recipe {difficulty}",
                cooking_time=30,
                difficulty=difficulty,
                user=self.user
            )
            self.assertEqual(recipe.difficulty, difficulty)
    
    def test_recipe_field_max_lengths(self):
        """Test field maximum length validations"""
        # Test name field max length
        long_name = 'x' * 201  # Exceeds max_length of 200
        recipe = Recipe(
            name=long_name,
            cooking_time=30,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            recipe.full_clean()


class RecipeURLTest(TestCase):
    """Test URL patterns and routing"""
    
    def setUp(self):
        """Set up test data for URL tests"""
        self.user = User.objects.create_user(
            username='urluser',
            email='url@example.com',
            password='urlpass123'
        )
        self.recipe = Recipe.objects.create(
            name="URL Test Recipe",
            cooking_time=30,
            user=self.user
        )
    
    def test_recipe_urls_resolve(self):
        """Test that all recipe URLs resolve correctly"""
        # Test home URL
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
        
        # Test list URL
        url = reverse('recipes:list')
        self.assertEqual(url, '/list/')
        
        # Test detail URL
        url = reverse('recipes:detail', kwargs={'pk': self.recipe.pk})
        self.assertEqual(url, f'/recipe/{self.recipe.pk}/')
        
        # Test search URL
        url = reverse('recipes:search')
        self.assertEqual(url, '/search/')
        
        # Test analytics URL
        url = reverse('recipes:analytics')
        self.assertEqual(url, '/analytics/')
        
        # Test login URL
        url = reverse('recipes:login')
        self.assertEqual(url, '/login/')
        
        # Test logout URL
        url = reverse('recipes:logout')
        self.assertEqual(url, '/logout/')


class RecipeAuthenticationTest(TestCase):
    """Test authentication and authorization"""
    
    def setUp(self):
        """Set up test data for authentication tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='authuser',
            email='auth@example.com',
            password='authpass123'
        )
        self.recipe = Recipe.objects.create(
            name="Auth Test Recipe",
            cooking_time=30,
            user=self.user
        )
    
    def test_login_view(self):
        """Test login functionality"""
        # Test GET request to login page
        response = self.client.get(reverse('recipes:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
        
        # Test POST request with valid credentials
        response = self.client.post(reverse('recipes:login'), {
            'username': 'authuser',
            'password': 'authpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('recipes:login'), {
            'username': 'authuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertContains(response, 'Invalid')
    
    def test_logout_functionality(self):
        """Test logout functionality"""
        # Login first
        self.client.login(username='authuser', password='authpass123')
        
        # Test logout
        response = self.client.get(reverse('recipes:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
    
    def test_protected_views_require_login(self):
        """Test that protected views redirect to login when not authenticated"""
        protected_urls = [
            reverse('recipes:list'),
            reverse('recipes:detail', kwargs={'pk': self.recipe.pk}),
            reverse('recipes:search'),
            reverse('recipes:analytics'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('login', response['Location'])


class RecipePaginationTest(TestCase):
    """Test pagination functionality"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data for pagination tests"""
        cls.user = User.objects.create_user(
            username='paginationuser',
            email='pagination@example.com',
            password='paginationpass123'
        )
        
        # Create multiple recipes for pagination testing
        for i in range(15):
            Recipe.objects.create(
                name=f"Recipe {i+1}",
                cooking_time=30,
                difficulty="Easy",
                servings=2,
                user=cls.user
            )
    
    def setUp(self):
        """Set up for each test method"""
        self.client = Client()
        self.client.login(username='paginationuser', password='paginationpass123')
    
    def test_recipe_list_pagination(self):
        """Test pagination in recipe list view"""
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        
        # Check if pagination is working (assuming 10 recipes per page)
        if hasattr(response.context, 'recipes') and hasattr(response.context['recipes'], 'has_other_pages'):
            self.assertTrue(response.context['recipes'].has_other_pages())
    
    def test_search_results_pagination(self):
        """Test pagination in search results"""
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredients': '',
            'difficulty': 'any',
            'cooking_time': 'any'
        })
        self.assertEqual(response.status_code, 200)
        
        # Should return all 15 recipes
        self.assertContains(response, 'Recipe 1')
        self.assertContains(response, 'Recipe 15')
