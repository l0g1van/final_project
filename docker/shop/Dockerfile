FROM python:3.10 as python-base

WORKDIR /home/appuser/app

COPY ./shop/requirements.txt .

 #apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt

COPY ./shop /home/appuser/app

ENV DJANGO_SETTINGS_MODULE=shop.settings
ENV SECRET_KEY=mysecretkey

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
