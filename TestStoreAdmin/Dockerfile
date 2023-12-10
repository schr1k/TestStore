FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3.11", "manage.py", "runserver", "0.0.0.0:8000"]