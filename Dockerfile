FROM python:3.11-slim

# Create non-root user
RUN useradd -m ctfuser

# Set working dir
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create DB during build time
RUN python vuln_api.py init-db

# Set DB permissions to be readable by app user
RUN chown -R ctfuser:ctfuser /app && chmod 644 /app/ctf.db

# Switch to non-root user
USER ctfuser

EXPOSE 5000
CMD ["python", "vuln_api.py"]
