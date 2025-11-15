from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),  # Welcome page at root
    path('list/', views.recipe_list, name='list'),  # Recipe list at /recipes/list/
]