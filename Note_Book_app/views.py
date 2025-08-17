from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Note
from django.views.generic import ListView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

#this class is for the first page that you face.the url is ./note_book
class main_page_view(LoginRequiredMixin,TemplateView):
    template_name = "main_page.html"

#this class is for the new note page that contains a form.
class new_note_view(LoginRequiredMixin,CreateView):
    template_name = "new_note.html"
    model = Note
    fields = ["name","note"]

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

#this is for the previous_note page that contains links to saved notes.
class previous_notes_view(LoginRequiredMixin,ListView):
    template_name="previous_notes.html"
    model= Note
    paginate_by=10
    ordering=['-Published_at']

#this function shows the detail of a created view.
class note_view(DetailView):
    model=Note
    template_name='note_detail.html'
    context_object_name = 'note'


#This function edit notes.
class edit_note_view(UpdateView):
    model=Note
    template_name='new_note.html'
    fields=["name","note"]
    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        response=super().post(request, *args, **kwargs)
        messages.success(request,f"the {self.object} was successfully edited!")
        return response

#this function delete notes.
class delete_note_view(DeleteView):
    model = Note
    template_name='delete_note_confirmation.html'
    success_url = reverse_lazy("Note_Book_app:previous_notes")
    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        response=super().post(request, *args, **kwargs)
        messages.success(request,f"the {self.object} was successfully deleted!")
        return response


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/signup.html'