# Recipe App

A Django-based recipe management application built as part of the CareerFoundry Python course.

## Features

- Recipe management with categories and difficulty levels
- Ingredient management with optional quantities
- User profiles and authentication
- Admin interface for easy content management
- Many-to-many relationships between recipes and ingredients

## Project Structure

- `manage.py` - Django management script
- `recipe_project/` - Main Django project configuration
- `recipes/` - Recipe and category models
- `ingredients/` - Ingredient management
- `users/` - User profile management

## Setup

1. Install dependencies:
   ```bash
   pip install django
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Run development server:
   ```bash
   python manage.py runserver
   ```

## Models

- **Recipe**: Name, cooking time, difficulty, ingredients
- **Ingredient**: Name with optional quantities per recipe
- **Category**: Recipe categorization
- **UserProfile**: Extended user information