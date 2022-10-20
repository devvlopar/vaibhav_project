
from email.policy import default
from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique = True)
    mobile = models.CharField(max_length = 15)
    password = models.CharField(max_length=50)
    pic = models.FileField(upload_to = 'profile', default= 'sad.jpg')

    def __str__(self) -> str:
        return self.first_name


class Blog(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    description = models.TextField()
    pic = models.FileField(upload_to='blogs', default= 'blog1.jpg')
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.title


class Donations(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.FloatField(default = 0.0)

    def __str__(self) -> str:
        return self.user + ' paid to ' + self.blog