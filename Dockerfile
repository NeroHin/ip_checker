# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the backend and frontend directories into the container
COPY backend /app/backend
COPY frontend /app/frontend

# Install any needed packages specified in requirements.txt
# Assuming you might use a requirements.txt for Python dependencies
RUN pip install flask flask_sqlalchemy

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Environment variable to serve the static files from the frontend directory
ENV STATIC_URL /static
ENV STATIC_PATH /app/frontend

# Run app.py when the container launches
CMD ["python", "backend/app.py"]