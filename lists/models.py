from django.db import models
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_lists', args=[self.id])

    def create_new(self):
        pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)  # ordering of Item.objects.all() queryset
        unique_together = ('list', 'text')

