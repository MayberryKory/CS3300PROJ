from rest_framework import serializers
from .models import *

class GrocerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GroceryItem
        fields = ['id', 'item_name', 'sku', 'cost']