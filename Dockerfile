FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services-pinger.py ./services-pinger.py

CMD [ "python", "./services-pinger.py" ]