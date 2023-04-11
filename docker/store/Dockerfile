FROM python:3.10-alpine as python-base

WORKDIR /app

COPY ../../store/requirements.txt /app/

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY ../../store/store /app/

ENV DJANGO_SETTINGS_MODULE=store.settings
ENV SECRET_KEY=mysecretkey

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]

