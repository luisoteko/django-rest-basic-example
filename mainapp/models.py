from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

class Note(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class NoteShare(models.Model):
    note = models.ForeignKey(Note, related_name='shares', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='shares', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('note', 'user')