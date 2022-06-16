from operator import mod
from statistics import mode
from turtle import ondrag
from django.db import models


from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    ticker = models.CharField(max_length=10, null=False, blank=False)
    buyDate = models.CharField(max_length=10, null=False, blank=False)
    sellDate = models.CharField(max_length=10, null=False, blank=False)
    percentChange = models.DecimalField(max_digits=19, decimal_places=2)
    graph = models.CharField(max_length=100, null=False, blank=False)
    caption = models.TextField(null=False, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    id = models.BigAutoField(primary_key=True)
    hex = models.CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return self.ticker


# @receiver(post_delete, sender=Post)
# def submission_delete(sender, instance, **kwargs):
#     instance.graph.delete(False)