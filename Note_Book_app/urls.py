from django.urls import path,include
from . import views


app_name="Note_Book_app"

urlpatterns = [
    path("",views.main_page_view.as_view(),name='main_page'),
    path("new_note",views.new_note_view.as_view(),name='new_note'),
    path("previous_notes",views.previous_notes_view.as_view(),name='previous_notes'),
    path("note/<int:pk>",views.note_view.as_view(),name='note_detail_page'),
    path("edit_note/<int:pk>",views.edit_note_view.as_view(),name='edit_note'),
    path("delete_note/<int:pk>",views.delete_note_view.as_view(),name='delete_note'),
]
