FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHON UNBUFFERED=1
CMD ["gunicorn","TMS.wsgi:application","--bind","0.0.0.0:8000"]
