from .models import User,Book

def getUserBooks(user):
	return Book.objects.filter(seller_id=user.id)