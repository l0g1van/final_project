FROM python:3.11-slim as python-base

RUN apt-get update --fix-missing && apt-get upgrade -qy

RUN apt update && apt install curl -y

FROM python-base as python-compile

COPY ./shop/requirements.txt .

RUN pip install --no-cache-dir -t /python -r requirements.txt

FROM python-base as hillel_example

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

COPY --from=python-compile /python /home/appuser/python
ENV PYTHONPATH=/home/appuser/python
ENV PATH="${PYTHONPATH}/bin:${PATH}"

COPY ./shop home/appuser/app
COPY ./docker/shop home/appuser/app/docker
WORKDIR /home/appuser/app

#RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-alpine-linux-amd64-v0.6.1.tar.gz && \
#    tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-v0.6.1.tar.gz

RUN chmod +x docker/runserver.sh docker/wait-for-command.sh docker/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/home/appuser/app/docker/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver"]