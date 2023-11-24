from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse  
from .models import *
from .views import *
from .forms import *

class IndexTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "groceries_app/index.html")

    def test_template_content(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, "<h3>Shop for the Best Prices</h3>")
        self.assertNotContains(response, "Not on the page")

class GroceryDetailPageTests(TestCase):
    def setUp(self):
        # Create a GroceryItem instance for testing purposes
        GroceryItem.objects.create(pk=1, item_name='Test Item', sku='12345', cost = '8.99')  

    def test_url_exists_at_correct_location(self):
        response = self.client.get(reverse("item-detail", kwargs={'pk': 1})) 
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("item-detail", kwargs={'pk': 1})) 
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("item-detail", kwargs={'pk': 1}))  
        self.assertTemplateUsed(response, "groceries_app/groceryitem_detail.html")

    def test_template_content(self):
        response = self.client.get(reverse("item-detail", kwargs={'pk': 1}))  
        self.assertContains(response, "<h1>Item Details</h1>")
        self.assertNotContains(response, "Should not be here!")

class GroceryItemModelTest(TestCase):
    def setUp(self):
        self.grocery_item = GroceryItem.objects.create(item_name="Test Item", sku="SKU123", cost=5.99)

    def test_item_str(self):
        self.assertEqual(str(self.grocery_item), "Test Item")

    def test_get_absolute_url(self):
        self.assertEqual(self.grocery_item.get_absolute_url(), reverse('item-detail', args=[str(self.grocery_item.id)]))


class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(recipe_name="Test Recipe", creator=self.user)

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), "Test Recipe")

    def test_get_absolute_url(self):
        self.assertEqual(self.recipe.get_absolute_url(), reverse('recipe-detail', args=[str(self.recipe.id)]))

    def test_recipe_has_ingredients(self):
        grocery_item = GroceryItem.objects.create(item_name="Ingredient", sku="SKU456", cost=2.5)
        self.recipe.recipe_ingredients.add(grocery_item)
        self.assertIn(grocery_item, self.recipe.recipe_ingredients.all())

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.grocery_item = GroceryItem.objects.create(item_name='Test Item', sku='SKU123', cost=5.99)
        self.recipe = Recipe.objects.create(recipe_name='Test Recipe', creator=self.user)
        self.recipe_list = RecipeList.objects.create(list_name='Test List')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groceries_app/index.html')

    def test_grocery_item_list_view(self):
        response = self.client.get(reverse('grocery-items'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groceries_app/groceryitem_list.html')

    def test_grocery_item_detail_view(self):
        response = self.client.get(reverse('item-detail', kwargs={'pk': self.grocery_item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groceries_app/groceryitem_detail.html')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe-detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groceries_app/recipe_detail.html')
    

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe-detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groceries_app/recipe_detail.html')


    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects after logout

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')

    def test_create_recipe_view_GET(self):
        response = self.client.get(reverse('create-recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groceries_app/recipe_form.html')


    def test_update_recipe_view_GET(self):
        response = self.client.get(reverse('update-recipe', kwargs={'recipe_id': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groceries_app/recipe_form.html')
    
    def test_delete_recipe_view_POST(self):
        response = self.client.post(reverse('delete-recipe', kwargs={'recipe_id': self.recipe.pk}))
        self.assertEqual(response.status_code, 302)  


class TestForms(TestCase):
    def test_grocery_item_form_valid(self):
        form_data = {
            'item_name': 'Test Item',
            'sku': 'SKU123',
            'cost': 5.99,
        }
        form = GroceryItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_grocery_item_form_invalid(self):
        # Test with invalid data for grocery item form
        form_data = {
            'item_name': '',
            'sku': 'SKU123',
            'cost': 'abc',  # Invalid cost
        }
        form = GroceryItemForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_recipe_form_valid(self):
        # Assuming there are GroceryItem instances in the database
        grocery_item = GroceryItem.objects.create(item_name='Test Item', sku='SKU123', cost=5.99)
        
        form_data = {
            'recipe_name': 'Test Recipe',
            'grocery_items': [grocery_item.pk],  # Use existing GroceryItem's primary key
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_form_invalid(self):
        # Test with invalid data for recipe form
        form_data = {
            'recipe_name': '',
            'grocery_items': [],  # No items selected
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_user_registration_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid(self):
        # Test with invalid data for user registration form
        form_data = {
            'username': '',
            'email': 'invalid-email',  # Invalid email format
            'password1': 'testpassword',
            'password2': 'differentpassword',  # Passwords don't match
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestAppFunctionality(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_recipe(self):
        # Simulate creating a new recipe through the app
        response = self.client.post(reverse('create-recipe'), {
            'recipe_name': 'New Recipe',
            # Add other necessary form data here
        })

        # Check if the recipe creation was successful (e.g., redirects to the detail page)
        self.assertRedirects(response, reverse('recipe-detail', kwargs={'pk': Recipe.objects.latest('id').pk}))


    def test_delete_recipe(self):
        # Create a recipe to delete
        recipe = Recipe.objects.create(recipe_name='Recipe to Delete', creator=self.user)

        # Simulate deleting the recipe through the app
        response = self.client.post(reverse('delete-recipe', kwargs={'recipe_id': recipe.pk}))

        # Check if the deletion was successful (e.g., redirects to the recipe list page)
        self.assertRedirects(response, reverse('recipes'))
        self.assertFalse(Recipe.objects.filter(pk=recipe.pk).exists())