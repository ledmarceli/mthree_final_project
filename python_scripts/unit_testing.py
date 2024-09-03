import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class WebAppTest(unittest.TestCase):
    
    def setUp(self):
        # Properly initialize ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("http://16.171.20.149:5000")  # Update with your actual Docker container port

    def test_functionality(self):
        driver = self.driver
        #Wait a moment for the page to load
        time.sleep(2)
        
        # Find fields
        first_name_field = driver.find_element("name", "first_name")
        last_name_field = driver.find_element("name", "last_name")
        income_field = driver.find_element("name", "income")
        expenses_field = driver.find_element("name", "expenses")
        submit_button = driver.find_element(By.XPATH, "//button[text()='Calculate Tax']")
        
        # Fill fields and submit
        first_name_field.send_keys("Marceli")
        last_name_field.send_keys("Ciesielski")
        income_field.send_keys("27000")
        expenses_field.send_keys("2000")
        submit_button.click()
        
        # Wait a moment for the page to load
        time.sleep(1)
        
        # Check if the output is fine
        self.assertIn("Tax Calculation Result", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()