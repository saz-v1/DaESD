FROM python:3.11

WORKDIR /app

RUN apt update && apt install -y libpq-dev gcc

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
