FROM python:3.11-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
COPY . .
EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]