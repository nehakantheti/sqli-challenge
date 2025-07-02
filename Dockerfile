FROM python:3.11-slim

# Create non-root user
RUN useradd -m ctfuser

# Set working dir
WORKDIR /app

# Copy files and fix permissions
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set permissions for /app and all its contents
RUN chown -R ctfuser:ctfuser /app

# Switch to non-root user
USER ctfuser

EXPOSE 5000
CMD ["python", "vuln_api.py"]
