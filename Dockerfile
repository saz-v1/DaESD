FROM python:3.11

WORKDIR /app

RUN apt update && apt install -y libpq-dev gcc netcat-openbsd

COPY . /app

RUN pip install -r requirements.txt
RUN python -m pip install -U 'channels[daphne]'

# Create media directory if it doesn't exist and set permissions
RUN mkdir -p /app/media/community_images && \
    chmod -R 777 /app/media

EXPOSE 8000

# Use entrypoint script to handle startup operations
ENTRYPOINT ["/app/entrypoint.sh"]
