------------------------
------ Vetusbooks ------
------------------------
Description : A place where you can merchandise old books.


Softwares Needed : 
	1. install "virtualenv" (used version 15.1.0)
	2. install "python3.4.0"
Environment Setup:
	1. create virtual environment with python3.4 with below command
		 
		 $ virtualenv -p python3.4 envname

		 in above command python3 is exact location of your installed python3.4

	2. all packages from requirements.txt using pip

		$ pip install -r requirements.txt

All Environment is set up:

Now you can place src in your trydjango and start using vetusbooks

Important Commands:

	1.To start project
		$ django-adming startproject projectname
	2.To Start an app
		$ django-admin startapp vetusbooks
	3. To Go to db Shell
		$ python manage.py shell
	4. To Start server in local Network
		$ python manage.py runserver 0.0.0.0:8000

To Make a user SuperUser:

1. Go to shell using above third command

	from vetusbook.models import User
	user = User.objects.get(username="your user name goes here")
	user.is_staff = True
	user.is_admin = True
	user.is_superuser = True
	user.save()

Models : 
	User:
		- username
		- password
		- emial
		- phone
		- location
		- avatar (profile pic)

	Book:
		- title
		- author
		- price
		- seller (foreignkey - references id in User model)
		- thumbnail (image field)
		- description