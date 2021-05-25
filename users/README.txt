source venv/bin/activate

or

pip install -r requirements.txt

python manage.py makemigrations core
python manage.py makemigrations users
python manage.py migrate