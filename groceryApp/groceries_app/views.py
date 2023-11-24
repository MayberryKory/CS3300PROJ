from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.urls import reverse_lazy
from .api_client import KrogerClient



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

# Login view
class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    authentication_form = AuthenticationForm
    

# Logout
def logut(request):
    auth_logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or login page
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    user_profile = request.user  # Accessing the current logged-in user
    return render(request, 'registration/profile.html', {'user_profile': user_profile})

@login_required
def createRecipe(request):
    form = RecipeForm()
    
    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        project_data = request.POST.copy()
        
        form = RecipeForm(project_data)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.creator = request.user
            recipe.save()
        
            # Redirect back to the portfolio detail page
            return redirect('recipe-detail', pk=recipe.id)

    context = {'form': form}
    return render(request, 'groceries_app/recipe_form.html', context)

@login_required
def deleteRecipe(request, recipe_id):
    
    recipe = Recipe.objects.get(pk=recipe_id)

    if request.method == 'POST':
        # Delete the project
        recipe.delete()
        return redirect('recipes')

    return render(request, 'groceries_app/project_delete.html', {'recipe': recipe})

@login_required
def updateRecipe(request, recipe_id):
    # Retrieve the existing recipe
    recipe = Recipe.objects.get(pk=recipe_id)

    if request.method == 'POST':
        # If the request method is POST, process the form data
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe-detail', recipe_id)  # Redirect to the recipe detail page

    else:
        # If the request method is GET, display the form with the existing data
        form = RecipeForm(instance=recipe)

    return render(request, 'groceries_app/recipe_form.html', {'form': form, 'recipe': recipe})

def grocery_items(request):
    client_id = "shopnest-c3f6a3ac62a8ec4c7a93f6c9aa42d1658272743587919993717"
    client_secret = "4yBG7MpD4bYi1imSjMkZQo-I9xsyTSStSlySV4Df"
    # Initialize the Kroger API client with your client credentials
    kroger_client = KrogerClient(client_id, client_secret)

    # Replace with the product ID and location ID you want to retrieve
    product_id = '0002100065883'
    # location_id = 'null'

    # Fetch data from Kroger's API using the client
    data = kroger_client.search_products(product_id=product_id)

    # Extract the data you need from the Kroger API response
    if data:
        kroger_item = data[0]  # Assuming the first result is the desired product

        # Map the data to your GroceryItem model
        grocery_item = GroceryItem(
            item_name=kroger_item.brand + ' ' + kroger_item.description,
            sku=kroger_item.upc,
            cost=kroger_item.price
        )

        # Save the GroceryItem object to your database
        grocery_item.save()

    # Retrieve all GroceryItem objects from the database
    grocery_item_list = GroceryItem.objects.all()

    context = {
        'grocery_item_list': grocery_item_list,
    }
    return render(request, 'groceries_app/groceryitem_list.html', context)


