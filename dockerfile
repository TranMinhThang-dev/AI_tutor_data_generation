# Use an official lightweight Python image.
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Preparing Manim dependencies and build tools
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y build-essential libcairo2-dev libpango1.0-dev pkg-config ffmpeg curl \
    texlive texlive-latex-extra texlive-fonts-extra texlive-latex-recommended texlive-science poppler-utils
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run run.py when the container launches
CMD ["python", "api.py"]

