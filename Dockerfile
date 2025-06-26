FROM node:18 AS frontend-builder

# Set the working directory
WORKDIR /frontend

# Copy frontend files
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy all frontend source code
COPY frontend/ ./
RUN npm run build

FROM python:3.12
LABEL author="Quang Minh"
LABEL description="A machine learning model serving API for personality prediction with React frontend"

# Set the working directory
WORKDIR /app

# Copy all backend files needed
COPY main.py /app/main.py
COPY server.py /app/server.py
COPY requirements.txt /app/requirements.txt
COPY run.py /app/run.py
# Try to copy model if it exists, but don't fail if it doesn't
COPY model.pkl* /app/

# Copy built frontend from the previous stage
COPY --from=frontend-builder /frontend/build /app/static

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8888

# Run the application with our wrapper script that ensures model exists
CMD ["python", "run.py"]