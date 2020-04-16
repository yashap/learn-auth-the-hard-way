FROM python:3.8-slim-buster

# COPY src/requirements.txt /usr/src/requirements.txt
COPY src /usr/src
WORKDIR /usr/src

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

ENTRYPOINT ["python"]
CMD ["app.py"]
