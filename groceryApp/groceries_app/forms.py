from django.forms import ModelForm
from django.forms import forms, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import GroceryItem, Recipe, RecipeList
from django.forms.formsets import formset_factory


# Create a form for GroceryItem
class GroceryItemForm(ModelForm):
    class Meta:
        model = GroceryItem
        fields = ('item_name', 'sku', 'cost')


class RecipeForm(ModelForm):
    grocery_items = ModelMultipleChoiceField(
        queryset=GroceryItem.objects.all(),
        widget= CheckboxSelectMultiple,  # You can use any widget you prefer
        required=False,  # You can set this to True if at least one item should be selected
    )

    class Meta:
        model = Recipe
        fields = ['recipe_name']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

        # If you want to prepopulate the form with selected items, you can do so here
        if self.instance.pk:
            self.fields['grocery_items'].initial = self.instance.recipe_ingredients.all()

    def save(self, commit=True):
        recipe = super(RecipeForm, self).save(commit=False)

        if commit:
            recipe.save()

        if recipe.pk:
            # Clear the existing grocery items and add the selected ones
            recipe.recipe_ingredients.set(self.cleaned_data['grocery_items'])

        return recipe


# Create a form for RecipeList
class RecipeListForm(ModelForm):
    class Meta:
        model = RecipeList
        fields = ('list_name', 'recipes', 'search_lowest_cost', 'preferred_store')


