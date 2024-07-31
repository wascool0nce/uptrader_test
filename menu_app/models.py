from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.url
