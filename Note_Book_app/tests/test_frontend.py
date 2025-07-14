from django.test import TestCase
from django.urls import reverse
from .django_modelfield_tests_funcs import *
from django.core.files.uploadedfile import SimpleUploadedFile
import re




# Create your tests here.

class Front_tests(TestCase):
    
    """this class is for frontend tests and tests the front functionality."""
    def setUp(self):
        self.url=reverse("Note_Book_app:main_page")
        self.response=self.client.get(self.url)
        
    def test_main_page_returns_200_status_code(self): #this func tests that the mainpage returns 200 status code.
        self.assertEqual(self.response.status_code,200)

    def test_main_page_uses_the_correct_template(self): #this func test that the main page uses the correct template.
        self.assertTemplateUsed(self.response,template_name="main_page.html")
        print("this context of the main page\n",self.response.content)
    
    def test_main_page_link_returns_200_status_code(self): #this func test that the user will redirect to a working page with 200 status code.
        self.response_main_page_links=[]
        html_bytes = self.response.content
        html_str = html_bytes.decode('utf-8')
        matches = re.findall(r'href="([^"]+)"', html_str)
        for i in range(0,len(matches)):
            self.response_main_page_links.append(self.client.get(matches))
        for i in range(0,len(self.response_main_page_links)):
            self.assertEqual(self.response_main_page_links,200)
 

    # def test_main_page_shows_correct_context(self): #this func test that the main page shows the correct context.
    #     self.assertEqual(self.response.context,self.context)