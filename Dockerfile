FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    build-essential \
    && apt-get clean

# Copy the requirements.txt file from your local machine to the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire BankProject folder (including manage.py) to the container
COPY BankProject /app/BankProject/

# Expose port 8000 for Django
EXPOSE 8000

# Set the default command to run the Django application
CMD ["python3", "/app/BankProject/manage.py", "runserver", "0.0.0.0:8000"]
