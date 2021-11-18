from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class news(models.Model):
    title =models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title[0:20]} --- {self.author.username}"
    
    class Meta: 
        verbose_name_plural = "News"
        


