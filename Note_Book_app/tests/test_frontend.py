from django.test import TestCase
from django.urls import reverse
from .django_modelfield_tests_funcs import *
import re
from Note_Book_app.models import Note
from bs4 import BeautifulSoup



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
    
    def test_main_page_link_returns_200_status_code(self): #this func test that the user will redirect to a working page with 200 status code.
        self.response_main_page_links=[]
        html_bytes = self.response.content
        html_str = html_bytes.decode('utf-8')
        matches = re.findall(r'href="([^"]+)"', html_str)
        for i in range(0,len(matches)):
            self.response_main_page_links.append(self.client.get(matches[i]))
        for i in range(0,len(self.response_main_page_links)):
            self.assertEqual(self.response_main_page_links[i].status_code,200)


    def test_new_note_page_post_data_returns_302_status_code(self): #this func tests that the new note page posts the data in its form return 302 status code.
        self.url_new_note= reverse("Note_Book_app:new_note")
        form_data = {
        'name': 'My Test Note',
        'note': 'This is the content sent from the frontend.'
        }
        new_note_page_post_res=self.client.post(path=self.url_new_note, data=form_data )
        self.assertEqual(new_note_page_post_res.status_code,302)
 
    def test_new_note_page_post_data_saved_correctly_in_database(self): #This function verifies if the data posted to the backend is stored correctly.
        self.url_new_note= reverse('Note_Book_app:new_note')
        form_data = {
        'name': 'My Test Note',
        'note': 'This is the content sent from the frontend.'
        }
        new_note_page_post_res=self.client.post(path=self.url_new_note, data=form_data )
        self.assertEqual(Note.objects.last().name,form_data['name'])
        self.assertEqual(Note.objects.last().note,form_data['note'])
    #from 
    def test_previous_page_shows_the_list_of_correctly(self): #Verifies that the note list page displays all notes correctly.
        for i in range(0,10):
            Note.objects.create(name=f'note{i}',note=f'context{i}')
        previous_page_url=reverse("Note_Book_app:previous_notes")
        res_previous_page=self.client.get(previous_page_url)
        # self.assertContains(self.res_previous_page.content.decode('utf-8'),str(Note.objects.all()[:10]))
        extracted_notes = []

        for item in list(Note.objects.all().order_by('-id')[:10]):
            s = str(item)  
            match = re.search(r'note\d+', s)
            if match:
                extracted_notes.append(match.group())

        soup = BeautifulSoup(res_previous_page.content, 'html.parser')
        notes_in_content = [a.get_text(strip=True) for a in soup.find_all('a')]
        self.assertEqual(notes_in_content,extracted_notes)


    def test_previous_note_page_links_to_related_notes_return_200_status_code(self): # Verifies that the Previous_note page links is related correctly to its note.
        for i in range(0,10):
            Note.objects.create(name=f'note{i}',note=f'context{i}')
        previous_page_url=reverse("Note_Book_app:previous_notes")
        res_previous_page=self.client.get(previous_page_url)
        html_str = res_previous_page.content.decode('utf-8')
        hrefs = re.findall(r'href="(/note_book/note/\d+)"', html_str)
        for i in range(0,10):
            self.assertEqual(self.client.get(hrefs[i]).status_code,200)

    def test_new_note_page_shows_the_expected_note(self): #Verfies that the new_note page shows the expected note.
        for i in range(0,10):
            Note.objects.create(name=f'note{i}',note=f'context{i}')
        previous_page_url=reverse("Note_Book_app:previous_notes")
        res_previous_page=self.client.get(previous_page_url)
        objects_name=[]
        objects_context=[]
        note_name_from_html=[]
        note_context_from_html=[]
        html_str = res_previous_page.content.decode('utf-8')
        hrefs = re.findall(r'href="(/note_book/note/\d+)"', html_str)
        print(self.client.get(hrefs[i]).content)
        for i in range(9,-1,-1):       
            objects_name.append(Note.objects.all()[i].name)
            objects_context.append(Note.objects.all()[i].note)
        for i in range(0,10):
            self.assertInHTML(objects_name[i],self.client.get(hrefs[i]).content.decode('utf-8'))
            self.assertInHTML(objects_context[i],self.client.get(hrefs[i]).content.decode('utf-8'))
            print(objects_name[i])
            print(objects_context[i])