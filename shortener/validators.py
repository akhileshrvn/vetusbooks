from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

def validate_url(value):
	url_validator = URLValidator()
	value_1_invalie = False
	value_2_invalid = False
	print(value)
	try:
		url_validator(value)
	except:
		value_1_invalie = True
	value_2_url = "http://"+value
	try:
		url_validator(value_2_url)
	except:
		value_2_invalid = True
	if value_1_invalie == False and value_2_invalid == False:
		raise ValidationError("Invalid URl for this field")
	return value

def validate_dot_com(value):
	if not "com" in value:
		raise ValidationError("This is  not valid because of no .com")
	return value