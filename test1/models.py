from django.db import models

# Create your models here. Models are to get information from database
from django.db import models
from django.utils import timezone


class ToDoItem(models.Model):
    text = models.CharField(max_length=100)
    due_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.text}: due {self.due_date}"

class Test(models.Model):
    title = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.title}:{self.value}"

class Test2(models.Model):
    text = models.CharField(max_length=100)
    due_date = models.DateField(default=timezone.now)

class Fromage(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.title}"