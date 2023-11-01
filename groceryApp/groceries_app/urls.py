from django.urls import path
from groceries_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('groceryItems/', views.GroceryItemListView.as_view(), name= 'grocery-items'),
    path('groceryItems/<int:pk>', views.GroceryItemDetailView.as_view(), name='item-detail'),
    path('recipes/', views.RecipeView.as_view(), name= 'recipes'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipeLists/', views.RecipeListListView.as_view(), name= 'recipe-lists'),
    path('recipeLists/<int:pk>', views.RecipeListDetailView.as_view(), name='recipe-lists-detail'),
    path('recipes/create_recipe/', views.createRecipe, name='create-recipe'),
    path('recipes/delete/<int:recipe_id>/', views.deleteRecipe, name='delete-recipe'),
    path('recipes/update_recipe/<int:recipe_id>', views.updateRecipe, name='update-recipe'),

]
