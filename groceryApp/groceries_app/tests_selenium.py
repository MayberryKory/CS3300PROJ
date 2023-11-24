from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse  
from .models import *
from .views import *
from .forms import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import os
import time
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class TestNavbarAndAuthentication(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.driver.get(self.live_server_url)
        test_user = User.objects.create(username='testuser')
        test_user.set_password('testpassword')
        test_user.save()
        time.sleep(2)

    def test_navbar_links(self):
        home_link = self.driver.find_element(By.LINK_TEXT, "Home")
        grocery_items_link = self.driver.find_element(By.LINK_TEXT, "Grocery Items")
        recipes_link = self.driver.find_element(By.LINK_TEXT, "Recipes")
        login_link = self.driver.find_element(By.LINK_TEXT, "Login")

        home_link.click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Grocery Items").click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Home").click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Recipes").click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Home").click()

        WebDriverWait(self.driver, 5).until(EC.title_contains("Grocery Aggregator Application"))
        self.assertIn("Grocery Aggregator Application", self.driver.title)


      

    def test_login_functionality(self):
        try:
            login_link = self.driver.find_element(By.LINK_TEXT, "Login")
            login_link.click()

            # Wait for the login form to be present
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "id_username")))

            username_field = self.driver.find_element(By.ID, 'id_username')
            password_field = self.driver.find_element(By.ID, 'id_password')
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

            # Using ActionChains for interacting with elements
            action = ActionChains(self.driver)
            action.move_to_element(username_field)
        
            action.click()
            
            action.send_keys('testuser')
            
            action.move_to_element(password_field)
            
            action.click()
            
            action.send_keys('testpassword')
            
            action.move_to_element(submit_button)
           
            action.click()
            
            action.perform()

            # Wait for the page to load after login and check for Welcome message
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome')]")))
            self.assertIn("Welcome", self.driver.page_source)

        except NoSuchElementException as e:
            # Log element not found exception for debugging
            print(f"Element not found: {e}")
            self.fail("One of the elements not found on the page")
        except TimeoutException:
            # Log timeout exception for debugging
            self.fail("Welcome message not found after login")
        except Exception as e:
            # Log any other unexpected exceptions for debugging
            print(f"An unexpected error occurred: {e}")
            self.fail("An unexpected error occurred during login")

