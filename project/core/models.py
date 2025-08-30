from django.db import models
from django.contrib.auth import get_user_model
from precise_bbcode.fields import BBCodeTextField

User=get_user_model()

class Post(models.Model):
    title=models.CharField(max_length=100)
    body=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=BBCodeTextField(default="")

    class Meta:
        permissions=[
            ("view_secret_post","Can view secret post")
        ]
    def __str__(self):
        return self.title