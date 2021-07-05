FROM python:3.7

RUN apt-get update
RUN apt-get -y install cmake
RUN apt-get -y install libglib2.0.0
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install build-essential
RUN apt-get install libx11-dev
RUN apt-get install python3-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 80

COPY .env .env

RUN mkdir -p /uploads/img

COPY ./app /app

ENV PYTHONPATH=.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
