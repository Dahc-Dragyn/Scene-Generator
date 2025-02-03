# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Install system dependencies for CUDA (if necessary)
# You might need to adjust these based on your specific CUDA/cuDNN version requirements.
# Check the NVIDIA website for the correct versions for your chosen GPU.
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-toolkit-11-8 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 8000

# Define environment variables (if needed)
ENV PORT=8000
ENV HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
ENV GEMINI_API_KEY=${GEMINI_API_KEY}
ENV PROJECT_ID=${PROJECT_ID}
ENV LOCATION=${LOCATION}

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]