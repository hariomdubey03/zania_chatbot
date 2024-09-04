# Zania Chatbot API

## Overview

The Zania Chatbot API allows you to interact with a chatbot service. This API provides an endpoint to submit documents and questions, which are then processed to return answers.


## Setup

To set up the development environment, follow these steps:

### 1. Create a virtual environment:

```bash
python3 -m venv env
```

### 2. Activate the virtual environment:
```bash
source env/bin/activate

```

### 3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run:
```bash
python3 main.py
```


## Base URL

http://localhost:8000


## Endpoint

### POST /zania/chat

This endpoint processes a PDF document and a JSON file containing questions. It returns answers in JSON format.

#### Request

**Method**: `POST`

**URL**: `/zania/chat`

**Headers**:
- `Content-Type`: `multipart/form-data`

**Body**: `form-data`
- `questions`: The JSON file containing questions to be answered.
  - **Type**: File
  - **Example Path**: `~/zania_chatbot//ai_chatbot/questions.json`
- `data`: The PDF file containing the data to be processed.
  - **Type**: File
  - **Example Path**: `~/zania_chatbot/ai_chatbot/theGoogleFileSystem.pdf`

#### Response

**Content-Type**: `application/json`

**Status Code**: `200 OK`

**Headers**:
- `Content-Disposition`: `attachment;filename=answers.json`
- `Content-Type`: `application/json`
- `Transfer-Encoding`: `chunked`

**Body**: JSON object containing answers to the questions. Example response:

```json
{
    "A GFS cluster consists of": "one master, two master replicas, 16 chunkservers, and 16 clients.",
    "what chunk size they have choosen ?": "They have chosen 64 MB as their chunk size.",
    "What GFS does not gurantee ?": "GFS does not provide any caching below the file system interface.",
    "Explain master replication": "Master replication is a technique used in the GFS (Google File System) for ensuring reliability. It involves replicating the state of the master (the central server that manages the file system) on multiple machines. This means that if the master fails, a backup can quickly take its place. Additionally, there are \"shadow\" masters that provide read-only access to the file system even when the primary master is down, with a slight lag. This helps enhance read availability for files that are not actively being changed. To stay updated, the shadow master constantly reads a replica of the master's state."
}
