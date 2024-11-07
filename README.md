# Question-Answering System Using Retrieval-Augmented Generation (RAG)

Welcome to the **Question-Answering System** project, which leverages Retrieval-Augmented Generation (RAG) to serve detailed, contextually relevant answers. This repository contains all necessary components for setting up a RAG-based question-answering system using Elasticsearch for document storage and retrieval, alongside an API for serving answers based on user queries.

---

## Contents

- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Elasticsearch Configuration](#elasticsearch-configuration)
- [Project Structure](#project-structure)

---

## Setup Instructions

Follow these steps to set up the environment, build the Docker image, and run the project.

### Prerequisites

- Docker installed on your system
- Internet access to download the necessary Docker images and dependencies

### Step-by-Step Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ishaanbassi/Question-Answering-using-RAG.git
   cd Question-Answering-using-RAG
   ```

2. **Build the Docker Image**

   Build the Docker image using the following command. The context for the Docker build should be the entire `Question-Answering-using-RAG` folder.

   ```bash
    sudo docker build -f .devcontainer/Dockerfile -t <image_name:image_version> .
   ```

3. **Running the Application**

   Use the command below to start the Docker container, exposing the necessary ports (9200 for Elasticsearch and 9202 for the API).

   ```bash
   docker run -p 9200:9200 -p 9202:9202 -v <path_to_pdfs>:/workspaces/qa/data --name <container_name> <image_name:image_version>
   
   ```

   Once the API has initialized, enter the openai key to run decoder for answer generation.

4. **API Health Check**
   
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
   - **Sample curl request**:
     ```bash
     curl -X POST http://localhost:9202/ask -H "Content-Type: application/json" -d '{"question": "What is the company policy on remote work?"}'
     ```

## Elasticsearch Configuration

This system uses Elasticsearch for storing and retrieving context passages for questions. Ensure that the configuration in the code aligns with your local or cloud-based Elasticsearch setup. The default port is 9200.

## Project Structure

- **Dockerfile**: Contains instructions for building the Docker image.
- **run.sh**: Shell script that waits for Elasticsearch to initialize, runs the document storage script, and starts the API.
- **store_documents.py**: Script for storing documents in Elasticsearch.
- **qa_api.py**: Main API script for serving question-answering requests.
- **config.json**: Project configuration, including models used for generating document embeddings and the final response to query
