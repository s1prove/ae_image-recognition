FROM python:3.9

RUN apt-get update && apt-get install python3 python3-pip -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

RUN pip3 install Flask numpy Pillow tensorflow 

COPY . /app

WORKDIR /app

RUN mkdir -p static/uploads static/decoded

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]

