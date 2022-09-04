FROM python:latest

WORKDIR /qr_bot

COPY . .

RUN pip install -r req.txt

CMD ["python", "main.py"]