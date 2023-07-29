# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the Python files to the container
COPY . .

# Install app dependencies
RUN pip install -r requirements.txt

# Expose port 8000 for the app
EXPOSE 8501

# Start the app
CMD streamlit run --server.port 8501 app.py
