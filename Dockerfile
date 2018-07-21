from python:3

MAINTAINER iamzjk@gmail.com

COPY . /app
WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "app/app.py"]