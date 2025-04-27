# Simple FastAPI MySQL API for Load Testing in microk8s

## Overview
This project provides a simple FastAPI-based API with two endpoints to insert and read items from a MySQL database. It is designed to be containerized and deployed in microk8s for load testing purposes.

## Endpoints
- `POST /items`: Insert an item with `name` and optional `description`.
- `GET /items`: Retrieve all items from the database.

## Setup

### Prerequisites
- MySQL database running and accessible.
- microk8s or Kubernetes cluster for deployment.
- Docker installed for building the container image.

### Environment Variables
Set the following environment variables to configure the database connection:
- `DB_HOST` (default: localhost)
- `DB_USER` (default: root)
- `DB_PASSWORD` (default: empty)
- `DB_NAME` (default: testdb)

### Database Schema
Create the `items` table in your MySQL database:
```sql
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);
```

### Build and Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Build Docker Image
```bash
docker build -t fastapi-mysql-api .
```

### Run Docker Container
```bash
docker run -d -p 8000:8000 \
  -e DB_HOST=your_db_host \
  -e DB_USER=your_db_user \
  -e DB_PASSWORD=your_db_password \
  -e DB_NAME=your_db_name \
  fastapi-mysql-api
```

## Usage
Use the API endpoints to insert and read items. This API can be used for load testing in microk8s.
