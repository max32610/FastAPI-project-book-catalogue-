FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PTHONNUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn","main:app"]