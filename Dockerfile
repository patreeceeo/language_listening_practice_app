FROM python:3.11-slim

# Install Node.js
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies and build CSS
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build:css

# Set up Django
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "language_listening_practice_app.wsgi:application", "--bind", "0.0.0.0:8000"]