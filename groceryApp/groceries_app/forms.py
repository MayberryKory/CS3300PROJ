from django.forms import ModelForm
from .models import GroceryItem, Recipe, RecipeList

# Create a form for GroceryItem
class GroceryItemForm(ModelForm):
    class Meta:
        model = GroceryItem
        fields = ('item_name', 'sku', 'cost')

# Create a form for Recipe
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('recipe_name', 'recipe_ingredients')

# Create a form for RecipeList
class RecipeListForm(ModelForm):
    class Meta:
        model = RecipeList
        fields = ('list_name', 'recipes', 'search_lowest_cost', 'preferred_store')
