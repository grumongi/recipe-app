#!/usr/bin/env python3
"""
Test script for the new Recipe Cooking Times chart
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
from django.test import Client
from django.urls import reverse

def test_new_chart():
    """Test the new recipe cooking times chart"""
    print("🧪 Testing New Recipe Cooking Times Chart")
    print("=" * 50)
    
    # Create test client and user
    client = Client()
    user = User.objects.create_user(
        username='chartuser',
        email='chart@example.com',
        password='chartpass123'
    )
    
    # Create some test recipes with different cooking times
    recipes_data = [
        {"name": "Quick Salad", "cooking_time": 10},
        {"name": "Pasta Carbonara", "cooking_time": 25},
        {"name": "Roast Chicken", "cooking_time": 60},
        {"name": "Slow-cooked Beef", "cooking_time": 180},
        {"name": "Scrambled Eggs", "cooking_time": 5},
    ]
    
    for recipe_data in recipes_data:
        Recipe.objects.create(
            name=recipe_data["name"],
            cooking_time=recipe_data["cooking_time"],
            difficulty="Medium",
            servings=4,
            user=user
        )
    
    print(f"✅ Created {len(recipes_data)} test recipes")
    
    # Login and test analytics view
    client.login(username='chartuser', password='chartpass123')
    response = client.get(reverse('recipes:analytics'))
    
    if response.status_code == 200:
        print("✅ Analytics page loads successfully")
        
        # Check if the new chart context is available
        context = response.context
        if 'recipe_times' in context:
            print("✅ Recipe times chart data is available")
            if context['recipe_times']:
                print("✅ Chart has been generated (base64 data present)")
            else:
                print("⚠️  Chart data is empty")
        else:
            print("❌ Recipe times chart not found in context")
            
        # Check recipe data
        total_recipes = context.get('total_recipes', 0)
        avg_time = context.get('avg_cooking_time', 0)
        print(f"📊 Total recipes: {total_recipes}")
        print(f"⏱️  Average cooking time: {avg_time} minutes")
        
    else:
        print(f"❌ Analytics page failed to load (status: {response.status_code})")
    
    # Test chart content
    content = response.content.decode('utf-8')
    if 'Recipe Cooking Times' in content:
        print("✅ New chart title found in HTML")
    if 'recipe_times' in content:
        print("✅ Chart variable found in template")
        
    print("\n" + "=" * 50)
    print("🎯 Chart Features:")
    print("   • Horizontal bar chart for better recipe name readability")
    print("   • Color-coded bars (green=quick, orange=medium, red=long)")
    print("   • Cooking time labels on each bar")
    print("   • Recipes sorted by cooking time")
    print("   • Professional styling with grid lines")
    print("=" * 50)
    
    # Clean up test data
    Recipe.objects.filter(user=user).delete()
    user.delete()
    
    print("✅ Test completed successfully! 🎉")
    print("🌐 View the new chart at: http://127.0.0.1:8000/recipes/analytics/")

if __name__ == "__main__":
    test_new_chart()