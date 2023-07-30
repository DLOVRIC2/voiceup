# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Python files to the container
COPY . .

# Expose port 8000 for the app
EXPOSE 8501

# Start the app
CMD streamlit run --server.port 8501 app.py
