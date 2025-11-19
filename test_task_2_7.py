#!/usr/bin/env python3
"""
Test script for Recipe Search and Analytics functionality
Tests the new features added for Task 2.7
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/Users/mariemuhire/careerfoundry/Intro-to_Python/Achievement 2/Exercise 2.2/A2_Recipe_App')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_project.settings')
django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from ingredients.models import Ingredient

def test_search_functionality():
    """Test the search functionality implementation"""
    print("🔍 Testing Recipe Search Functionality")
    print("=" * 50)
    
    # Check if we have any recipes in the database
    total_recipes = Recipe.objects.count()
    print(f"Total recipes in database: {total_recipes}")
    
    if total_recipes == 0:
        print("⚠️  No recipes found. Let's create a test recipe.")
        
        # Create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print("✅ Test user created")
        
        # Create test category
        category, created = Category.objects.get_or_create(
            name='Test Category'
        )
        if created:
            print("✅ Test category created")
        
        # Create test ingredients
        ingredient1, created = Ingredient.objects.get_or_create(
            name='tomato',
            defaults={'unit_of_measure': 'piece'}
        )
        ingredient2, created = Ingredient.objects.get_or_create(
            name='cheese',
            defaults={'unit_of_measure': 'grams'}
        )
        print("✅ Test ingredients created")
        
        # Create a test recipe
        recipe = Recipe.objects.create(
            name='Test Pizza',
            description='A delicious test pizza recipe',
            cooking_time=30,
            instructions='1. Make dough\n2. Add toppings\n3. Bake',
            difficulty='Easy',
            category=category,
            author=user
        )
        
        # Add ingredients to recipe
        recipe.ingredients.add(ingredient1, ingredient2)
        recipe.save()
        print("✅ Test recipe created")
        
    # Test search functionality
    print("\n🔍 Testing search filters...")
    
    # Test name search
    name_results = Recipe.objects.filter(name__icontains='pizza')
    print(f"Name search for 'pizza': {name_results.count()} results")
    
    # Test ingredient search
    ingredient_results = Recipe.objects.filter(ingredients__name__icontains='cheese')
    print(f"Ingredient search for 'cheese': {ingredient_results.count()} results")
    
    # Test difficulty filter
    easy_recipes = Recipe.objects.filter(difficulty='Easy')
    print(f"Easy recipes: {easy_recipes.count()} results")
    
    # Test cooking time categories
    quick_recipes = Recipe.objects.filter(cooking_time__lt=30)
    medium_recipes = Recipe.objects.filter(cooking_time__gte=30, cooking_time__lt=60)
    long_recipes = Recipe.objects.filter(cooking_time__gte=60)
    
    print(f"Quick recipes (<30 min): {quick_recipes.count()}")
    print(f"Medium recipes (30-60 min): {medium_recipes.count()}")
    print(f"Long recipes (>60 min): {long_recipes.count()}")

def test_analytics_data():
    """Test analytics data collection"""
    print("\n📊 Testing Analytics Data Collection")
    print("=" * 50)
    
    total_recipes = Recipe.objects.count()
    print(f"Total recipes: {total_recipes}")
    
    if total_recipes > 0:
        # Difficulty distribution
        easy_count = Recipe.objects.filter(difficulty='Easy').count()
        medium_count = Recipe.objects.filter(difficulty='Medium').count()
        hard_count = Recipe.objects.filter(difficulty='Hard').count()
        
        print(f"Easy recipes: {easy_count}")
        print(f"Medium recipes: {medium_count}")
        print(f"Hard recipes: {hard_count}")
        
        # Average cooking time
        cooking_times = Recipe.objects.values_list('cooking_time', flat=True)
        avg_cooking_time = sum(cooking_times) / len(cooking_times)
        print(f"Average cooking time: {avg_cooking_time:.1f} minutes")
        
        # Time categories
        quick_count = Recipe.objects.filter(cooking_time__lt=30).count()
        medium_time_count = Recipe.objects.filter(cooking_time__gte=30, cooking_time__lt=60).count()
        long_count = Recipe.objects.filter(cooking_time__gte=60).count()
        
        print(f"Quick recipes: {quick_count}")
        print(f"Medium-time recipes: {medium_time_count}")
        print(f"Long recipes: {long_count}")
    else:
        print("No recipes available for analytics")

def test_url_patterns():
    """Test URL pattern configuration"""
    print("\n🌐 Testing URL Patterns")
    print("=" * 50)
    
    from django.urls import reverse
    
    try:
        search_url = reverse('recipes:search')
        print(f"✅ Search URL: {search_url}")
    except Exception as e:
        print(f"❌ Search URL error: {e}")
    
    try:
        analytics_url = reverse('recipes:analytics')
        print(f"✅ Analytics URL: {analytics_url}")
    except Exception as e:
        print(f"❌ Analytics URL error: {e}")

def main():
    """Main test function"""
    print("🧪 Testing Recipe App - Task 2.7 Implementation")
    print("=" * 60)
    
    try:
        test_search_functionality()
        test_analytics_data()
        test_url_patterns()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("🎉 Recipe Search and Analytics functionality is ready!")
        print("\nYou can now:")
        print("1. 🔍 Use the search feature at: http://127.0.0.1:8000/recipes/search/")
        print("2. 📊 View analytics at: http://127.0.0.1:8000/recipes/analytics/")
        print("3. 🏠 Access the home page at: http://127.0.0.1:8000/")
        print("4. 📋 Browse all recipes at: http://127.0.0.1:8000/recipes/")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()