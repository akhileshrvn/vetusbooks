from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_phone
import os
# Create your models here.

def get_user_books_path(instance, filename):
	print("Before Instance Id :"+str(instance.seller_id))
	return os.path.join('books', str(instance.seller_id), filename)

class User(AbstractUser):
	phone = models.CharField(max_length=10, unique=True, validators=[validate_phone], blank=False)
	location = models.CharField(max_length = 30, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	avatar = models.ImageField(upload_to = 'avatar', default = 'avatar/avatar.jpg')

class Book(models.Model):
	title = models.CharField(max_length=100, blank=False)
	author = models.CharField(max_length=100, blank=False)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	thumbnail = models.ImageField(upload_to=get_user_books_path, blank=True, null=True)
	description = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.title + " by " + self.author +" for " + str(self.price) + "rs."