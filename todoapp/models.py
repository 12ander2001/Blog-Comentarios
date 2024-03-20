from django.db import models
from django.contrib.auth.models import User

class todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=1000, null=False, blank=True, unique=True)
    status = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.todo_name



    def __str__(self):
        return self.todo_name
    
class Comment(models.Model):
    todo_item = models.ForeignKey(todo, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return self.text