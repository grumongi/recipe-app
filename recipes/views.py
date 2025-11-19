from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Recipe
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import io
import base64

# Create your views here.

def home(request):
    """Welcome page for the Recipe App"""
    return render(request, 'recipes/recipes_home.html')

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or the page they were trying to access
            next_url = request.GET.get('next', 'recipes:list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'recipes/login.html')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    return render(request, 'recipes/success.html')

@login_required
def recipe_list(request):
    """Display all recipes with their ingredients - Protected view"""
    recipes = Recipe.objects.all().select_related('category', 'user').prefetch_related('recipeingredient_set__ingredient')
    return render(request, 'recipes/list.html', {'recipes': recipes})

@login_required
def recipe_detail(request, pk):
    """Display detailed view of a single recipe - Protected view"""
    recipe = get_object_or_404(Recipe, pk=pk)
    # Recalculate difficulty to ensure it's current
    calculated_difficulty = recipe.calculate_difficulty()
    
    context = {
        'recipe': recipe,
        'calculated_difficulty': calculated_difficulty,
        'ingredients_list': recipe.get_ingredients_list(),
    }
    return render(request, 'recipes/detail.html', context)

@login_required
def search_recipes(request):
    """Search recipes with multiple criteria"""
    recipes_df = pd.DataFrame()
    search_performed = False
    
    if request.method == 'POST' or request.GET.get('show_all'):
        search_performed = True
        
        # Start with all recipes
        recipes = Recipe.objects.all().select_related('category', 'user').prefetch_related('recipeingredient_set__ingredient')
        
        if request.method == 'POST':
            # Get search criteria
            recipe_name = request.POST.get('recipe_name', '').strip()
            ingredients = request.POST.get('ingredients', '').strip()
            difficulty = request.POST.get('difficulty', '')
            cooking_time = request.POST.get('cooking_time', '')
            
            # Apply search filters
            if recipe_name:
                recipes = recipes.filter(name__icontains=recipe_name)
            
            if ingredients:
                # Search in ingredient names (wildcard search)
                recipes = recipes.filter(
                    ingredients__name__icontains=ingredients
                ).distinct()
            
            # Convert to list for difficulty filtering
            recipe_list = list(recipes)
            
            if difficulty and difficulty != 'any':
                # Filter by difficulty
                recipe_list = [recipe for recipe in recipe_list 
                             if recipe.calculate_difficulty().lower() == difficulty.lower()]
            
            if cooking_time and cooking_time != 'any':
                if cooking_time == 'quick':
                    recipe_list = [r for r in recipe_list if r.cooking_time < 30]
                elif cooking_time == 'medium':
                    recipe_list = [r for r in recipe_list if 30 <= r.cooking_time <= 60]
                elif cooking_time == 'long':
                    recipe_list = [r for r in recipe_list if r.cooking_time > 60]
            
            recipes = recipe_list
        else:
            # Show all recipes
            recipes = list(recipes)
        
        # Create DataFrame
        if recipes:
            df_data = []
            for recipe in recipes:
                df_data.append({
                    'id': recipe.pk,
                    'name': recipe.name,
                    'cooking_time': recipe.cooking_time,
                    'difficulty': recipe.calculate_difficulty(),
                    'ingredients': ', '.join(recipe.get_ingredients_list()[:3]) + ('...' if len(recipe.get_ingredients_list()) > 3 else '')
                })
            
            recipes_df = pd.DataFrame(df_data)
    
    context = {
        'recipes_df': recipes_df,
        'search_performed': search_performed,
        'recipes_count': len(recipes_df) if not recipes_df.empty else 0
    }
    
    return render(request, 'recipes/search.html', context)

@login_required
def analytics_view(request):
    """Display data analytics with charts"""
    
    # Get all recipes for analysis
    recipes = Recipe.objects.all()
    
    # Convert to DataFrame
    recipe_data = []
    for recipe in recipes:
        recipe_data.append({
            'name': recipe.name,
            'cooking_time': recipe.cooking_time,
            'difficulty': recipe.calculate_difficulty(),
            'created_date': recipe.created_date,
            'category': recipe.category.name if recipe.category else 'Uncategorized'
        })
    
    df = pd.DataFrame(recipe_data)
    
    # Generate charts
    charts = {}
    
    if not df.empty:
        # 1. Bar Chart - Recipes by Difficulty
        plt.figure(figsize=(10, 6))
        difficulty_counts = df['difficulty'].value_counts()
        x_labels = list(difficulty_counts.index)
        y_values = list(difficulty_counts.values)
        
        bars = plt.bar(x_labels, y_values, color=['#2ecc71', '#f39c12', '#e74c3c'])
        plt.title('Recipes by Difficulty Level', fontsize=16, fontweight='bold')
        plt.xlabel('Difficulty Level', fontsize=12)
        plt.ylabel('Number of Recipes', fontsize=12)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(y_values[i])}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        chart1_data = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        plt.close()
        charts['difficulty_bar'] = chart1_data
        
        # 2. Pie Chart - Cooking Time Categories
        plt.figure(figsize=(8, 8))
        time_categories = []
        for time in df['cooking_time']:
            if time < 30:
                time_categories.append('Quick (<30 min)')
            elif time <= 60:
                time_categories.append('Medium (30-60 min)')
            else:
                time_categories.append('Long (>60 min)')
        
        time_df = pd.Series(time_categories)
        time_counts = time_df.value_counts()
        
        labels = list(time_counts.index)
        sizes = list(time_counts.values)
        colors = ['#3498db', '#f39c12', '#e74c3c']
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Recipe Distribution by Cooking Time', fontsize=16, fontweight='bold')
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        chart2_data = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        plt.close()
        charts['time_pie'] = chart2_data
        
        # 3. Bar Chart - Recipe Names vs Cooking Time
        plt.figure(figsize=(14, 8))
        
        # Sort recipes by cooking time for better visualization
        df_sorted = df.sort_values('cooking_time', ascending=True)
        recipe_names = list(df_sorted['name'])
        cooking_times = list(df_sorted['cooking_time'])
        
        # Create color map based on cooking time (gradient from green to red)
        colors = []
        max_time = max(cooking_times) if cooking_times else 60
        for time in cooking_times:
            if time < 20:
                colors.append('#27ae60')  # Green for quick recipes
            elif time < 40:
                colors.append('#f39c12')  # Orange for medium recipes  
            else:
                colors.append('#e74c3c')  # Red for long recipes
        
        # Create horizontal bar chart for better recipe name readability
        plt.barh(recipe_names, cooking_times, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
        
        plt.title('Recipe Cooking Times', fontsize=16, fontweight='bold')
        plt.xlabel('Cooking Time (minutes)', fontsize=12)
        plt.ylabel('Recipe Names', fontsize=12)
        
        # Add time labels on bars
        for i, v in enumerate(cooking_times):
            plt.text(v + max_time * 0.01, i, f'{v} min', va='center', fontweight='bold')
        
        # Add a grid for easier reading
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        chart3_data = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        plt.close()
        charts['recipe_times'] = chart3_data
    
    context = {
        'difficulty_chart': charts.get('difficulty_bar', ''),
        'time_chart': charts.get('time_pie', ''),
        'recipe_times': charts.get('recipe_times', ''),
        'total_recipes': len(df),
        'avg_cooking_time': round(df['cooking_time'].mean(), 1) if not df.empty else 0,
        'easy_count': len([x for x in df['difficulty'] if x == 'Easy']) if not df.empty else 0,
        'medium_count': len([x for x in df['difficulty'] if x == 'Medium']) if not df.empty else 0,
        'hard_count': len([x for x in df['difficulty'] if x == 'Hard']) if not df.empty else 0,
        'quick_count': len([x for x in df['cooking_time'] if x < 30]) if not df.empty else 0,
    }
    
    return render(request, 'recipes/analytics.html', context)
