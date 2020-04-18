from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followlist = models.ManyToManyField("User", related_name="followers")
    likes = models.ManyToManyField("Posting", related_name="like", default=0)

class Posting(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=280)
    username = models.ForeignKey("User", on_delete=models.CASCADE, related_name="postings")

    def __str__(self):
        return self.description
