from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('groceryItems/', views.GroceryItemListView.as_view(), name= 'grocery-items'),
    path('groceryItems/<int:pk>', views.GroceryItemDetailView.as_view(), name='grocery-item-detail'),
    path('recipes/', views.RecipeView.as_view(), name= 'recipes'),
    path('recipes/<int:pk>', views.RecipeDetailView.as_view(), name='recipes-detail'),
    path('recipeLists/', views.RecipeListListView.as_view(), name= 'recipe-lists'),
    path('recipeLists/<int:pk>', views.RecipeListDetailView.as_view(), name='recipe-lists-detail'),
]
