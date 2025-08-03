from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Note
from django.views.generic import ListView,DetailView
from django.urls import reverse_lazy


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
    paginate_by=10
    ordering=['-Published_at']

#this function shows the detail of a created view.
class note_view(DetailView):
    model=Note
    template_name='note_detail.html'
    context_object_name = 'note'


class edit_note_view(UpdateView):
    model=Note
    template_name='new_note.html'
    fields=["name","note"]

class delete_note_view(DeleteView):
    model = Note
    template_name='delete_note.html'
    success_url = reverse_lazy("Note_Book_app:delete_note")