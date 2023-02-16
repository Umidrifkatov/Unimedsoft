FROM python:3.11-slim-buster
ENV PYTHONBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app


RUN python3 manage.py makemigrations core
RUN python3 manage.py makemigrations 
RUN python3 manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell