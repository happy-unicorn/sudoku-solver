FROM python:3.8.2
RUN mkdir /code
WORKDIR /code
ADD requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt