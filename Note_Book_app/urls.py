from django.urls import path

from . import views

app_name="Note_Book_app"

urlpatterns = [
    path("",views.main_page_view.as_view(),name='main_page'),
    path("new_note/",views.new_note_view.as_view(),name='new_note'),
    path("perevious_notes",views.perevious_notes_view.as_view(),name='perevious_notes'),
]
