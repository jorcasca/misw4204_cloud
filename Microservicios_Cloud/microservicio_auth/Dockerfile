FROM python:3.9-slim-buster

WORKDIR /microservicio_auth

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0
ENV SECRET_KEY=frase-secreta

EXPOSE 5000

CMD celery -A microservicio_auth.tareas.config.celery_app worker --loglevel=INFO & flask run --host=0.0.0.0 --port=5000

