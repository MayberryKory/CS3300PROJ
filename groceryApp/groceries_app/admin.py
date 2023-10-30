from django.contrib import admin
from .models import GroceryItem, Recipe, RecipeList

# Register your models here.
admin.site.register(GroceryItem)
admin.site.register(Recipe)
admin.site.register(RecipeList)