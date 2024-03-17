# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /application

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code and all the files to the working directory
COPY . /application

# Expose the port on which the application will run
EXPOSE 5000

# Run the FASTAPI application using the uvicorn server.
CMD ["python", "-m", "flask", "--app", "client.py", "run", "port", "5050"]