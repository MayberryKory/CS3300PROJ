from django.db import models
from django.urls import reverse

class GroceryItem(models.Model):
    item_name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200)
    cost = models.FloatField()

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])
                       

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    recipe_ingredients = models.ManyToManyField(GroceryItem)  

    def __str__(self):
        return self.recipe_name

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[str(self.id)])

class RecipeList(models.Model):
    list_name = models.CharField(max_length=200)
    recipes = models.ManyToManyField(Recipe)  
    search_lowest_cost = models.BooleanField(default=False)  

    GROCERYSTORES = (
        ('Krog', 'King Soopers/ City Market'),
        ('WalM', 'Walmart'),
        ('Sprt', 'Sprouts'),
        ('CosC', 'CostCo'),
    )
    preferred_store = models.CharField(
        max_length=4,  
        choices=GROCERYSTORES,
        blank=True
    )

    def __str__(self):
        return self.list_name

    def get_absolute_url(self):
        return reverse('list-detail', args=[str(self.id)])