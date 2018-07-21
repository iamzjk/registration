from python:3

MAINTAINER iamzjk@gmail.com

COPY . /
WORKDIR /

RUN pip install pipenv

RUN pipenv install --system --deploy

EXPOSE 8000

CMD ["gunicorn", "-b", "127.0.0.1:8000", "app.app:app", "--reload", '-w', '4']