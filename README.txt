pip install -r requirements.txt
python manage.py makemigrations users
python manage.py makemigrations core
python manage.py migrate