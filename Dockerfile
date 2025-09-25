# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim


# Set environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
libxml2-dev \
libxslt-dev \
libffi-dev \
&& rm -rf /var/lib/apt/lists/*


# Set workdir
WORKDIR /app


# Copy requirements first for better caching
COPY requirements.txt /app/requirements.txt


# Install python dependencies
RUN pip install --upgrade pip && pip install -r /app/requirements.txt


# Copy app source
COPY . /app


# Create non-root user and switch
RUN useradd -m appuser && chown -R appuser /app
USER appuser


# Expose port
EXPOSE 5000


# Entrypoint (use gunicorn in production; fallback to flask run for dev)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
