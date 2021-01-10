FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install -y libpq-dev 
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-w 4", "-b :8000", "wsgi:app"]
