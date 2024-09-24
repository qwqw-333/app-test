FROM python:3.9-slim

# Work dir
WORKDIR /app

# Requirements
COPY ../requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Else code copy
COPY ../ .

# Open port
EXPOSE 80

# Start
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:80"]
