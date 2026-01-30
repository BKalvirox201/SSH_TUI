FROM python:3.14.2
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8022

CMD ["python", "main.py"]

