from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),  # Welcome page at root
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('list/', views.recipe_list, name='list'),  # Recipe list at /list/ (protected)
    path('recipe/<int:pk>/', views.recipe_detail, name='detail'),  # Recipe detail at /recipe/id/ (protected)
    path('search/', views.search_recipes, name='search'),  # Recipe search page (protected)
    path('analytics/', views.analytics_view, name='analytics'),  # Analytics page (protected)
]