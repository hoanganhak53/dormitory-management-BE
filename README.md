# Dormitory Management - Backend

This project is a backend implementation for a dormitory management system built using FastAPI. It provides a robust API for managing various aspects of a dormitory, such as student information, room allocation, and registration. The backend utilizes a clustering algorithm to efficiently allocate students to dormitory rooms based on specific criteria.

## Installation

Follow the steps below to install and run the Dormitory Management backend project:

1. Clone the repository:

   ```shell
   git clone https://github.com/hoanganhak53/KTX-BE.git

2. Navigate to the project directory:
   ```shell
   cd dormitory-management-backend

3. Install the dependencies::
   ```shell
   pip install -r requirements.txt

4. Build and run the Docker container:
   ```shell
   docker-compose up -d

5. Start the FastAPI server:
   ```shell
    uvicorn main:app --reload

The application will be running at http://localhost:8001.

Follow this guide to creat nginx cert: https://learn.microsoft.com/en-us/azure/container-instances/container-instances-container-group-ssl
