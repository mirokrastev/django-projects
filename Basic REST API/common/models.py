from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class List(models.Model):
    title = models.CharField(max_length=25, null=False)
    content = models.CharField(max_length=150, null=True)
    owner = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)
