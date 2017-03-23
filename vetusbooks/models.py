from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_phone
# Create your models here.

class User(AbstractUser):
	phone = models.CharField(max_length=10, unique=True, validators=[validate_phone], blank=False)
	location = models.CharField(max_length = 30, blank=True)
	birth_date = models.DateField(null=True, blank=True)

class Book(models.Model):
	title = models.CharField(max_length=100, blank=False)
	author = models.CharField(max_length=100, blank=False)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	seller = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title + " by " + self.author +" at " + str(self.price) + "rs."

class ExampleModel(models.Model):
	model_pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')