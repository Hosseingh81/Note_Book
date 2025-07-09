from django.db import models

# Create your models here.

class Note(models.Model):
    default_name=f"note {id}"
    name=models.CharField(default=default_name)
    note=models.TextField(verbose_name="write your note here.")