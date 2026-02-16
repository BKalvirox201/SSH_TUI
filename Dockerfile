FROM python:3.14-slim
RUN apt-get update && apt-get install -y \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN chmod 600 ssh/ssh_host_key
RUN chmod 644 ssh/ssh_host_key.pub
RUN python -m pip install -r requirements.txt
EXPOSE 8022
CMD ["python", "main.py"]
