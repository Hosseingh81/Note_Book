from django.urls import path

from . import views

app_name="Note_Book_app"

urlpatterns = [
    path("",views.main_page_view.as_view(),name='main_page'),
]
