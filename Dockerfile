# Use the official Python image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE capstone_UI.settings

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy your Django project files into the container
COPY . /app/

# Run makemigrations and migrate in a custom setup script
COPY setup.sh /app/
RUN chmod +x /app/setup.sh
RUN /app/setup.sh

# Expose the port your Django app will run on
EXPOSE 8000

# Run migrations and start the production server using Gunicorn
#CMD ["gunicorn", "capstone_UI.wsgi:application", "--bind", "0.0.0.0:8001"]

# Run migrations and start the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
