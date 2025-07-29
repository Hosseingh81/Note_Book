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
        self.url_new_note= reverse("Note_Book_app:new_note")


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
        form_data = {
        'name': 'My Test Note',
        'note': 'This is the content sent from the frontend.'
        }
        new_note_page_post_res=self.client.post(path=self.url_new_note, data=form_data )
        self.assertEqual(new_note_page_post_res.status_code,302)
 

    def test_new_note_page_post_data_saved_correctly_in_database(self): #This function verifies if the data posted to the backend is stored correctly.
        form_data = {
        'name': 'My Test Note',
        'note': 'This is the content sent from the frontend.'
        }
        self.client.post(path=self.url_new_note, data=form_data )
        self.assertEqual(Note.objects.last().name,form_data['name'])
        self.assertEqual(Note.objects.last().note,form_data['note'])


    def test_previous_page_shows_the_list_of_notes_correctly(self): #Verifies that the note list page displays all notes correctly.
        for i in range(0,10):
            Note.objects.create(name=f'note{i}',note=f'context{i}')
        previous_page_url=reverse("Note_Book_app:previous_notes")
        res_previous_page=self.client.get(previous_page_url)
        html_str=res_previous_page.content.decode('utf-8')
        notes_in_content = re.findall(r'<a href="\/note_book\/note\/\d+">(note\d+)<\/a>', html_str)
        notes_in_content = notes_in_content[::-1]
        
        extracted_notes = []

        for item in list(Note.objects.all().order_by('-id')[:10]):
            s = str(item)  
            match = re.search(r'note\d+', s)
            if match:
                extracted_notes.append(match.group())

        for i in range(0,10):
            self.assertEqual(notes_in_content[i],extracted_notes[i])

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
        html_str = res_previous_page.content.decode('utf-8')
        hrefs = re.findall(r'href="(/note_book/note/\d+)"', html_str)
        for i in range(0,10):       
            objects_name.append(Note.objects.all()[i].name)
            objects_context.append(Note.objects.all()[i].note)
        for i in range(0,10):
            self.assertInHTML(objects_name[i],self.client.get(hrefs[i]).content.decode('utf-8'))
            self.assertInHTML(objects_context[i],self.client.get(hrefs[i]).content.decode('utf-8'))

        
    def test_edit_note_page_returns_200_status_code(self): #Verifies that edit_note page returns 200 status code.
        Note.objects.create(note="note 0")
        note_id=Note.objects.last().id
        edit_note_res=self.client.get(reverse("Note_Book_app:edit_note",kwargs={'pk':note_id}))
        self.assertEqual(edit_note_res.status_code,200)





    