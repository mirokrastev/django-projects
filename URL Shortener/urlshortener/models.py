from django.db import models


class URLModel(models.Model):
    url = models.URLField(max_length=1024, null=False, blank=False)
    alias = models.CharField(max_length=128, null=False, blank=True, unique=True)

    def __str__(self):
        return f'{self.url}:{self.alias}'
