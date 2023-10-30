from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from models import *
from forms import *

# Create your views here.
def index(request):
    return render(request, 'groceries_app/index.html')

class GroceryItemListView(generic.ListView):
    model = GroceryItem

class GroceryItemDetailView(generic.DetailView):
    model = GroceryItem

class RecipeView(generic.ListView):
    model = Recipe

class RecipeDetailView(generic.DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        context = True
        # Make this do something
        return context

class RecipeListListView(generic.ListView):
    model = RecipeList

class RecipeListDetailView(generic.DetailView):
    model = RecipeList