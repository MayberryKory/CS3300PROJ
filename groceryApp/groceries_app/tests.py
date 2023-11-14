from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse  


class IndexTests(SimpleTestCase):
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

class GroceryDetailPageTests(SimpleTestCase):  
    def test_url_exists_at_correct_location(self):
        response = self.client.get("grocery-items")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("grocery-items"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("grocery-items"))
        self.assertTemplateUsed(response, "groceries_app/groceryitem_detail.html")

    def test_template_content(self):
        response = self.client.get(reverse("grocery-items"))
        self.assertContains(response, "<h1>Item Details</h1>")
        self.assertNotContains(response, "Should not be here!")
