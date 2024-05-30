# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Create a Python virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Activate the virtual environment
RUN /bin/bash -c "source $VIRTUAL_ENV/bin/activate"

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app ./app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
