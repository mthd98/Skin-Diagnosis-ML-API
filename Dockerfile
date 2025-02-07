# Use Python 3.11
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /Skin-Diagnosis-ML-API
COPY . /Skin-Diagnosis-ML-API


# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Expose the FastAPI default port
EXPOSE 8000


# Define environment variable
ENV PORT 8080

WORKDIR  /Skin-Diagnosis-ML-API/App
# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "Main:app", "--host", "0.0.0.0", "--port", "8000"]
