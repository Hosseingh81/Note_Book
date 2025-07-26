from django.db import models
from django.urls import reverse

# Create your models here.

class Note(models.Model):
    name=models.CharField(blank=True)
    note=models.TextField(verbose_name="write your note here.")
    Published_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("Note_Book_app:previous_notes")
    

    def save(self,*args, **kwargs):
        creating=self.pk is None
        super().save(*args, **kwargs)


        if creating and not self.name:
            self.name = f"note {self.pk}"
            super().save(update_fields=['name'])