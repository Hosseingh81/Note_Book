from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Note
from django.views.generic import ListView

# Create your views here.

#this class is for the first page that you face.the url is ./note_book
class main_page_view(TemplateView):
    template_name = "main_page.html"

#this class is for the new note page that contains a form.
class new_note_view(CreateView):
    template_name = "new_note.html"
    model = Note
    fields = ["name","note"]

#this is for the previous_note page that contains links to saved notes.
class previous_notes_view(ListView):
    template_name="previous_notes.html"
    model= Note
    queryset=Note.objects.order_by('-id')[:10]