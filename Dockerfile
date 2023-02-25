FROM python:3.11-alpine
WORKDIR /app
EXPOSE 8000
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]