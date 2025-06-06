 README.md (setup)

1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python manage.py makemigrations && python manage.py migrate`
4. `python manage.py runserver`
5. Visit `/register`, `/login`, `/chat`

Also uncomment line 9 in chatbot/views.py and line 46 in settings.py

To start the front end follow the README.md instructions in frontendui folder. Just npm run dev should suffice. Once the frontend server is up access localhost:3000/register and /login.
