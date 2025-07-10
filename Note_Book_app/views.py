from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

#this class is for the first page that you face.the url is ./note_book
class main_page_view(TemplateView):
    template_name = "main_page.html"

