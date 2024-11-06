# Question-Answering System Using Retrieval-Augmented Generation (RAG)

Welcome to the **Question-Answering System** project, which leverages Retrieval-Augmented Generation (RAG) to serve detailed, contextually relevant answers. This repository contains all necessary components for setting up a RAG-based question-answering system using Elasticsearch for document storage and retrieval, alongside an API for serving answers based on user queries.

---

## Contents

- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Elasticsearch Configuration](#elasticsearch-configuration)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## Setup Instructions

Follow these steps to set up the environment, build the Docker image, and run the project.

### Prerequisites

- Docker installed on your system
- Internet access to download the necessary Docker images and dependencies

### Step-by-Step Setup

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd Question-Answering-using-RAG
   ```

2. **Build the Docker Image:**

   Build the Docker image using the following command. The context for the Docker build should be the entire `Question-Answering-using-RAG` folder.

   ```bash
   docker build -t temp:1.0.0 .
   ```

3. **Run the Docker Container:**

   Use the command below to start the Docker container, exposing the necessary ports (9200 for Elasticsearch and 9202 for the API).

   ```bash
   docker run -p 9200:9200 -p 9202:9202 --name testcode temp:1.0.0
   ```

## Running the Application

After starting the container, the system should initialize and launch both Elasticsearch and the API for question-answering. To verify that the API is running, you can send a `GET` request to the health check endpoint at `http://localhost:9202/health`.

Example health check command:

```bash
curl -X GET http://localhost:9202/health
```

If the system is running correctly, you should see a response indicating the API status as `healthy`.

## API Documentation

### Endpoints

1. **Health Check:**  
   - **URL**: `/health`
   - **Method**: `GET`
   - **Description**: Returns the status of the API.

2. **Question-Answering Endpoint:**  
   - **URL**: `/ask`
   - **Method**: `POST`
   - **Description**: Accepts a JSON payload containing a question and returns a generated answer along with relevant contexts.
   - **Request Payload**: 
     ```json
     {
       "question": "Your question here"
     }
     ```

## Elasticsearch Configuration

This system uses Elasticsearch for storing and retrieving context passages for questions. Ensure that the configuration in the code aligns with your local or cloud-based Elasticsearch setup. The default port is 9200.

## Project Structure

- **Dockerfile**: Contains instructions for building the Docker image.
- **run.sh**: Shell script that waits for Elasticsearch to initialize, runs the document storage script, and starts the API.
- **store_documents.py**: Script for storing documents in Elasticsearch.
- **qa_api.py**: Main API script for serving question-answering requests.

## Troubleshooting

If you encounter issues during setup or execution, consider the following:

- **Permission Issues**: Ensure that the Docker container user has sufficient permissions for all mounted volumes.
- **Elasticsearch Errors**: Check Elasticsearch logs for errors, and ensure the required ports are accessible.
- **API Not Responding**: Verify that all necessary ports are forwarded correctly and that the container is running without errors.

---

Thank you for using the Question-Answering System! For additional help, please consult the documentation or reach out to the project maintainers.
``` 

This markdown file includes all steps and sections in a consistent format. Let me know if further changes are needed!