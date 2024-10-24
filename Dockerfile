# Use the official Python image from the Docker Hub
FROM python:3.10-bullseye

# Set the working directory
WORKDIR /app

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "0_🏠_Home_Page.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
