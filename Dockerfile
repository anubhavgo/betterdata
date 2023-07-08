FROM python:3.11.1-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

EXPOSE 8000
WORKDIR /app
COPY ./requirements.txt .
COPY ./ . 
RUN pip install -r requirements.txt # Install the dependencies
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]