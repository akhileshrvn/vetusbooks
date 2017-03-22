from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
def validate_phone(value):
	phone_regex_string = r'^[\d]{10}$';
	phone_regex = re.compile(phone_regex_string)
	print(phone_regex.search(value)) 
	if not phone_regex.search(value):
		raise ValidationError(
				('%(value)s is not a valid phone number '),
				params={'value':value},
			)