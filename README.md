# Recipe Management System - Task 2.7

A comprehensive Django-based recipe management application with advanced search, analytics, and user authentication features. Built as part of the CareerFoundry Python for Web Developers course.

## 🚀 Features

### Core Functionality
- **Recipe Management**: Create, view, edit recipes with categories, difficulty levels, and images
- **Ingredient System**: Many-to-many relationships with optional quantities
- **User Authentication**: Secure login/logout with protected views
- **Admin Interface**: Comprehensive admin panel for content management

### Advanced Task 2.7 Features
- **🔍 Advanced Search**: Multi-criteria search with wildcards (*recipe*, ingredients, difficulty, cooking time)
- **📊 Analytics Dashboard**: Interactive charts and statistics
  - Difficulty distribution pie chart
  - Recipe cooking times horizontal bar chart  
- **📈 Smart Insights**: AI-powered recipe collection analysis
- **🎨 Professional UI**: Modern, responsive design with intuitive navigation
- **✅ Comprehensive Testing**: 24 test cases covering all functionality

## 🗂️ Project Structure

```
recipe-app/
├── manage.py                    # Django management script
├── recipe_project/             # Main Django project configuration
│   ├── settings.py            # Project settings (SECRET_KEY secured)
│   └── urls.py                # Main URL configuration
├── recipes/                    # Recipe management app
│   ├── models.py              # Recipe, Category models
│   ├── views.py               # Search, analytics, CRUD views
│   ├── urls.py                # App URL patterns
│   ├── admin.py               # Enhanced admin interface
│   ├── templates/recipes/     # HTML templates
│   │   ├── recipes_home.html  # Welcome page
│   │   ├── list.html          # Recipe listing
│   │   ├── detail.html        # Recipe detail view
│   │   ├── search.html        # Advanced search interface
│   │   ├── analytics.html     # Analytics dashboard
│   │   └── login.html         # User authentication
│   ├── test_comprehensive.py  # Complete test suite (24 tests)
│   └── image_mapping.py       # Image management utilities
├── ingredients/                # Ingredient management
├── users/                     # User profile management
├── media/                     # Recipe images and media files
└── test_*.py                  # Additional testing files
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Django 5.2.8
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/grumongi/recipe-app.git
   cd recipe-app
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django pandas matplotlib
   ```

4. **Configure environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   # Edit .env and set your DJANGO_SECRET_KEY
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data** (optional):
   ```bash
   python manage.py shell
   # Add sample recipes via admin or shell
   ```

8. **Run development server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the application**:
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 🔧 Usage

### Navigation
- **Home**: Welcome page with feature overview
- **Recipes**: Browse all recipes with filtering
- **Search**: Advanced multi-criteria search with wildcards
- **Analytics**: Interactive dashboard with charts and insights
- **Admin**: Content management (admin users only)

### Search Features
- **Name Search**: Use wildcards (*pasta*, *chicken*)
- **Ingredient Filter**: Search by specific ingredients
- **Difficulty**: Easy, Medium, Hard filtering
- **Cooking Time**: Quick (<30min), Medium (30-60min), Long (>60min)

### Analytics Features
- **Recipe Statistics**: Total count, average cooking time, difficulty distribution
- **Visual Charts**: Pie charts and horizontal bar charts
- **Smart Insights**: Automated analysis of your recipe collection

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python manage.py test

# Run specific test suites
python manage.py test recipes.test_comprehensive -v 2

# Test coverage includes:
# - Model validation (Recipe, Category, User relationships)
# - View functionality (CRUD, search, analytics)
# - Authentication and authorization
# - Form validation and constraints
# - URL routing and accessibility
# - Search functionality with all criteria
# - Analytics calculations and chart generation
```

**Test Results**: 24 tests covering all functionality - All PASSING ✅

## 🔒 Security Features

- **SECRET_KEY Protection**: Moved to environment variables
- **Authentication Required**: Protected views for logged-in users
- **Input Validation**: Comprehensive form and model validation
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **CSRF Protection**: Built-in Django CSRF protection

## 📊 Models

### Recipe Model
- `name`: Recipe title
- `description`: Detailed recipe description  
- `cooking_time`: Time in minutes
- `difficulty`: Easy/Medium/Hard choices
- `servings`: Number of servings
- `instructions`: Step-by-step cooking instructions
- `image`: Recipe photo upload
- `category`: Foreign key to Category
- `user`: Foreign key to User (recipe owner)

### Category Model
- `name`: Category name
- `description`: Category description
- `image`: Category image

### Ingredient Integration
- Many-to-many relationship through `RecipeIngredient`
- Optional quantities per recipe
- Searchable ingredient database

## 🎯 Task 2.7 Requirements Completion

✅ **Enhanced User Interface**: Modern, responsive design  
✅ **Advanced Search**: Multi-criteria with wildcards (*term*)  
✅ **Analytics Dashboard**: Interactive charts and insights  
✅ **Data Visualization**: Matplotlib charts with base64 encoding  
✅ **Comprehensive Testing**: 24 test cases covering all functionality  
✅ **Security Implementation**: SECRET_KEY protection, authentication  
✅ **Documentation**: Complete README and code documentation  
✅ **Git Management**: Proper version control with clean commits  

## 🚀 Deployment Notes

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Use environment variables for all sensitive data
5. Configure proper logging
6. Set up media file storage (AWS S3, etc.)

## 🤝 Contributing

This project is part of a educational assignment. For improvements or issues:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📝 License

Educational project for CareerFoundry Python for Web Developers course.

## 👨‍💻 Author

**Marie Muhire** - CareerFoundry Student  
- GitHub: [@grumongi](https://github.com/grumongi)
- Project: [Recipe Management System](https://github.com/grumongi/recipe-app)

---

**Achievement 2 - Exercise 2.7**: Django Web Application with Advanced Features ✅