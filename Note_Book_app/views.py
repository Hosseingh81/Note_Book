from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

#this class is for the first page that you face.the url is ./note_book
class main_page_view(TemplateView):
    template_name = "main_page.html"

#this class is for the new note page that contains a form.
class new_note_view(TemplateView):
    template_name = "new_note.html"

#this is for the previous_note page that contains links to saved notes.
class perevious_notes_view(TemplateView):
    template_name="pervious_notes.html"
