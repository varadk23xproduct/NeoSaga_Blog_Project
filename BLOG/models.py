from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class BlogPost(models.Model):
    title = models.CharField(max_length=150) 
    content = models.TextField()
    image = models.ImageField(upload_to='blog_image/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(default=now)

    def __str__(self):  
        return self.title
