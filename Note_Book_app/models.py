from django.db import models
from django.urls import reverse

# Create your models here.

class Note(models.Model):
    default_name=f"note {id}"
    name=models.CharField(default=default_name)
    note=models.TextField(verbose_name="write your note here.")
    Published_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("Note_Book_app:previous_notes")