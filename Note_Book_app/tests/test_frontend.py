from django.test import TestCase
from django.urls import reverse
from .django_modelfield_tests_funcs import *
import re
from Note_Book_app.models import Note
from django.contrib.messages import get_messages
from django.contrib.auth.models import User



# Create your tests here.

class Front_tests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test', password='123')
    
    """this class is for frontend tests and tests the front functionality."""
    def setUp(self):
        self.url=reverse("Note_Book_app:main_page")
        self.url_new_note= reverse("Note_Book_app:new_note")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>        main_page_test

    def test_main_page_redirects_anonymous_user_to_login(self): #Verfies that anonymous user can't access the main_page and it will redirect to login_page.
        self.response=self.client.get(self.url)
        self.assertEqual(self.response.status_code,302)
        self.assertEqual(self.response.headers.get('Location'),'/accounts/login/?next=/note_book/')


    def test_main_page_returns_200_status_code(self): #this func tests that the mainpage returns 200 status code.
        self.client.force_login(self.user)
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,200)


    def test_main_page_uses_the_correct_template(self): #this func test that the main page uses the correct template.
        self.client.force_login(self.user)
        response=self.client.get(self.url)
        self.assertTemplateUsed(response,template_name="main_page.html")
    
    def test_main_page_link_returns_200_status_code(self): #this func test that the user will redirect to a working page with 200 status code.
        self.client.force_login(self.user)
        response=self.client.get(self.url)
        self.response_main_page_links=[]
        html_bytes = response.content
        html_str = html_bytes.decode('utf-8')
        matches = re.findall(r'href="([^"]+)"', html_str)
        for i in range(0,len(matches)):
            self.response_main_page_links.append(self.client.get(matches[i]))
        for i in range(0,len(self.response_main_page_links)):
            self.assertEqual(self.response_main_page_links[i].status_code,200)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>        new_note_page_test
    
    def test_new_note_page_redirects_anonymous_user_to_login(self): #Verfies that anonymous user can't access the new_note_page and it will redirect to login_page.
        response=self.client.get(self.url_new_note)
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.headers.get('Location'),'/accounts/login/?next=/note_book/new_note')


    def test_new_note_page_post_data_returns_302_status_code(self): #this func tests that the new note page posts the data in its form return 302 status code.
        self.client.force_login(self.user)
        form_data = {
        'name': 'My Test Note',
        'note': 'This is the content sent from the frontend.'
        }
        new_note_page_post_res=self.client.post(path=self.url_new_note, data=form_data )
        self.assertEqual(new_note_page_post_res.status_code,302)
 

    def test_new_note_page_post_data_saved_correctly_in_database(self): #This function verifies if the data posted to the backend is stored correctly.
        self.client.force_login(self.user)
        form_data = {
        'name': 'My Test Note',
        'note': 'This is the content sent from the frontend.'
        }
        self.client.post(path=self.url_new_note, data=form_data )
        self.assertEqual(Note.objects.last().name,form_data['name'])
        self.assertEqual(Note.objects.last().note,form_data['note'])


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>        previous_notes_page_test


    def test_previous_notes_page_redirects_anonymous_user_to_login(self): #Verfies that anonymous user can't access the previous_notes_page and it will redirect to login_page.
        previous_page_url=reverse("Note_Book_app:previous_notes")
        response=self.client.get(previous_page_url)
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.headers.get('Location'),'/accounts/login/?next=/note_book/previous_notes')

    def test_previous_page_shows_the_list_of_notes_correctly(self): #Verifies that the note list page displays all notes correctly.
        self.client.force_login(self.user)
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
        self.client.force_login(self.user)
        for i in range(0,10):
            Note.objects.create(name=f'note{i}',note=f'context{i}')
        previous_page_url=reverse("Note_Book_app:previous_notes")
        res_previous_page=self.client.get(previous_page_url)
        html_str = res_previous_page.content.decode('utf-8')
        hrefs = re.findall(r'href="(/note_book/note/\d+)"', html_str)

        for i in range(0,10):
            self.assertEqual(self.client.get(hrefs[i]).status_code,200)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>        detail_note_page_test


    # def test_detail_note_page_shows_the_expected_note(self): #Verfies that the new_note page shows the expected note.
    #     for i in range(0,10):
    #         Note.objects.create(name=f'note{i}',note=f'context{i}')
    #     previous_page_url=reverse("Note_Book_app:previous_notes")
    #     res_previous_page=self.client.get(previous_page_url)
    #     objects_name=[]
    #     objects_context=[]
    #     html_str = res_previous_page.content.decode('utf-8')
    #     hrefs = re.findall(r'href="(/note_book/note/\d+)"', html_str)
    #     for i in range(0,10):       
    #         objects_name.append(Note.objects.all()[i].name)
    #         objects_context.append(Note.objects.all()[i].note)
    #     for i in range(0,10):
    #         self.assertContains(self.client.get(hrefs[i]),objects_name[i])
    #         self.assertContains(self.client.get(hrefs[i]),objects_context[i])


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>        edit_note_page_test

        
    def test_edit_note_page_returns_200_status_code(self): #Verifies that edit_note page returns 200 status code.
        Note.objects.create(note="note 0")
        note_id=Note.objects.last().id
        edit_note_res=self.client.get(reverse("Note_Book_app:edit_note",kwargs={'pk':note_id}))
        self.assertEqual(edit_note_res.status_code,200)


    def test_edit_note_page_post_request_retruns_302_status_code(self): #Verifies that a POST request to the edit_note page returns a 302 status code.
        Note.objects.create(name="note 0",note='context 0')
        note_id=Note.objects.last().id
        form_data = {
        'name': 'Edited Note',
        'note': 'This is the edited content sent from the frontend.'
        }
        edit_note_res=self.client.post(path=reverse("Note_Book_app:edit_note",kwargs={'pk':note_id}),data=form_data)
        self.assertEqual(edit_note_res.status_code,302)



    def test_edit_note_post_updates_note_object(self): #Verifies that submitting the edit form successfully updates the note in the database.
        Note.objects.create(name="note 0",note='context 0')
        note_id=Note.objects.last().id
        form_data = {
        'name': 'Edited Note 0',
        'note': 'edited context 0.'
        }
        edit_note_res=self.client.post(path=reverse("Note_Book_app:edit_note",kwargs={'pk':note_id}),data=form_data)
        self.assertEqual(form_data["name"],Note.objects.last().name)
        self.assertEqual(form_data["note"],Note.objects.last().note)


    def test_editing_note_displays_success_message(self): #Verifies that a success message is displayed after a note is edited.
        Note.objects.create(note="note 0")
        edit_note__url=reverse("Note_Book_app:edit_note",kwargs={'pk':Note.objects.get(note='note 0').id})
        form_data = {
        'name': 'Edited Note 0',
        'note': 'edited context 0.'
        }
        edit_note_post_res=self.client.post(edit_note__url,kwargs={'pk':Note.objects.get(note='note 0').id},data=form_data)
        messages = list(get_messages(edit_note_post_res.wsgi_request))
        redirected_url_from_edit_note_page=edit_note_post_res.headers.get('Location')
        response=self.client.get(redirected_url_from_edit_note_page)
        self.assertContains(response,messages[0])   




#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>        delete_note_page_test



    def test_detail_page_contains_valid_delete_link(self): #Verifies that the detail_page contains valid delete_link and delete_link returns 200 status code.
        Note.objects.create(note="note 0")
        note_id=Note.objects.last().id
        edit_note_res=self.client.get(reverse("Note_Book_app:note_detail_page",kwargs={'pk':note_id}))
        html_str=edit_note_res.content.decode('utf-8')
        match = re.search(r'/note_book/delete_note/\d+', html_str)
        delete_note_res=self.client.get(match.group())
        self.assertEqual(delete_note_res.status_code,200)



    def test_delete_note_confirmation_page_uses_correct_template(self): #Verifies that the delete_note_confiramation_page uses the correct template.
        Note.objects.create(note="note 0")
        delete_note_confirmation_res=self.client.get(reverse("Note_Book_app:delete_note",kwargs={'pk':Note.objects.last().id}))
        self.assertTemplateUsed(delete_note_confirmation_res,template_name='delete_note_confirmation.html')


    def test_delete_note_confirmation_page_post_redirects_to_previous_notes_page_and_delete_the_specified_note(self): #Verifies that when the user accept the deletation, it will redirects to previous_notes page and it deletes the specified note.
        Note.objects.create(note="note 0")
        expected_redirect_url=reverse("Note_Book_app:previous_notes")
        note_id=Note.objects.get(note='note 0').id
        delete_note_confirmation_url=reverse("Note_Book_app:delete_note",kwargs={'pk':note_id})
        delete_note_confirmation_post_res=self.client.post(delete_note_confirmation_url,kwargs={'pk':note_id})
        self.assertEqual(delete_note_confirmation_post_res.status_code,302)
        redirected_url_from_delete_note_confimation_page=delete_note_confirmation_post_res.headers.get('Location')
        self.assertEqual(redirected_url_from_delete_note_confimation_page,expected_redirect_url)
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note_id)


    # def test_deleting_note_displays_success_message(self): #Verifies that a success message is displayed after a note is deleted.
    #     Note.objects.create(note="note 0")
    #     delete_note_confirmation_url=reverse("Note_Book_app:delete_note",kwargs={'pk':Note.objects.get(note='note 0').id})
    #     delete_note_confirmation_post_res=self.client.post(delete_note_confirmation_url,kwargs={'pk':Note.objects.get(note='note 0').id})
    #     messages = list(get_messages(delete_note_confirmation_post_res.wsgi_request))
    #     redirected_url_from_delete_note_confimation_page=delete_note_confirmation_post_res.headers.get('Location')
    #     response=self.client.get(redirected_url_from_delete_note_confimation_page)
    #     self.assertContains(response,messages[0])



    def test_note_creation_assigns_correct_user(self):
        self.client.force_login(self.user)
        form_data = {
        'name': 'Edited Note 0',
        'note': 'edited context 0.'
        }
        new_note_page_post_res=self.client.post(path=self.url_new_note, data=form_data )
        self.assertEqual(new_note_page_post_res.wsgi_request.user,Note.objects.last().user)

        

