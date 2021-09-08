FROM python:3.9.1
ADD . /python-flask
WORKDIR /python-flask
EXPOSE 8000
RUN pip install -r requirements.txt