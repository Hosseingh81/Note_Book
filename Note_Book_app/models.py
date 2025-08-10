from django.db import models
from django.urls import reverse

# Create your models here.

class Note(models.Model):
    """
    this function is the Note model of the Note_Book_app of the Note_Book django project.
    in front of each field and each function you can see it's discription.
    """
    name=models.CharField(blank=True) # this is the name field of the model.
    note=models.TextField(verbose_name="write your note here.") #this is the note field of the model.
    Published_at=models.DateTimeField(auto_now_add=True) #this is published_at field of the model that saves the time whenever note is published.
    Update_at=models.DateTimeField(auto_now=True) #this is Upadted_at field of the model that stores the time when the object is updated.

    def __str__(self): # shows the name field of the note.
        return self.name
    
    def get_absolute_url(self): #Returns the canonical URL for a single note instance.
        return reverse("Note_Book_app:note_detail_page", kwargs={'pk': self.pk})
    

    def save(self,*args, **kwargs): #this function auto generate field name from pk if field name is null.
        super().save(*args, **kwargs)

        if not self.name:
            self.name = f"note {self.pk}"
            super().save(update_fields=['name'])