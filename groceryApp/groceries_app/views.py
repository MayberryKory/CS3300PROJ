from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *



# Create your views here.
def index(request):
    return render(request, 'groceries_app/index.html')

class GroceryItemListView(generic.ListView):
    model = GroceryItem
    context_object_name = "grocery_item_list"

class GroceryItemDetailView(generic.DetailView):
    model = GroceryItem
    context_object_name ="grocery_item"
class RecipeView(generic.ListView):
    model = Recipe

class RecipeDetailView(generic.DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class RecipeListListView(generic.ListView):
    model = RecipeList

class RecipeListDetailView(generic.DetailView):
    model = RecipeList

def createRecipe(request):
    form = RecipeForm()
    
    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        project_data = request.POST.copy()
        
        form = RecipeForm(project_data)
        if form.is_valid():
            recipe = form.save(commit=True)
        
            # Redirect back to the portfolio detail page
            return redirect('recipe-detail', pk=recipe.id)

    context = {'form': form}
    return render(request, 'groceries_app/recipe_form.html', context)

def deleteRecipe(request, recipe_id):
    
    recipe = Recipe.objects.get(pk=recipe_id)

    if request.method == 'POST':
        # Delete the project
        recipe.delete()
        return redirect('recipes')

    return render(request, 'portfolio_app/project_delete.html', {'recipe': recipe})


