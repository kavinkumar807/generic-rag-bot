# (GENERIC-RAG-BOT)

This project includes two applications: **streamlit** (frontend) and **FastAPI** (backend). The following instructions will guide you to run them individually or together.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Running streamlit (Frontend)](#running-streamlit-frontend)
- [Running FastAPI (Backend)](#running-fastapi-backend)
- [Running Both streamlit and FastAPI Together](#running-both-streamlit-and-fastapi-together)

## Prerequisites

Before running the applications, ensure that you have the following installed on your system:

- Python 3.x (recommended: 3.10 or higher)
- `pip` package manager
- Docker (if you are using Docker containers)
- Docker Compose (if you are using Docker Compose)

If not installed, follow the installation guides:
- [Python Installation Guide](https://www.python.org/downloads/)
- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

## Folder Structure

root/


├─── backend/                    
├─── frontend/                         
├─── data/           
├─── helper/                    
├─── public/                                   
├─── venv/                       
├─── .dockerignore               
├─── .env                        
├─── .gitignore                 
├─── app.py                     
├─── docker-compose.yaml         
├─── README.md                   
├─── requirements.txt  

## Environment Variables
Make sure to add the variables in .env file before running the application

```bash
GROQ_API_KEY= ... here ....
MONGO_API_KEY= .... here ....
etc
```

## Running streamlit (Frontend)

1. Navigate to the `frontend` directory.
2. Required plugins have already been installed as part c-one initialization
3. To run the streamlit application, use the following command:

```bash
streamlit run ui.py
```
This will start the streamlit application, and you can access it by visiting:

```bash
http://localhost:8501
```

## Running FastAPI (Backend)
1. Navigate to the `backend` directory.
2. Required plugins have already been installed as part c-one initialization.

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

This will start the FastAPI server, and you can access the backend by visiting:

```bash
http://localhost:8000
```

## Running Both streamlit and FastAPI Together

If you want to run both streamlit and FastAPI together in a unified environment, follow these steps:

1. Ensure both `frontend` and `backend` are set up properly (as described above).
2. You can run both applications using the following command in the root directory:

```bash
python app.py
```
This command will start both streamlit and FastAPI applications simultaneously.

* streamlit (Frontend) will be available at: `http://localhost:8501`
* FastAPI (Backend) will be available at: `http://localhost:8000`

## Docker Usage (Optional)
If you'd like to run both applications in Docker containers, ensure the following:
1. Build the Docker images by running:

```bash
docker-compose build
```
2. Start the services using Docker Compose:
```bash
docker-compose up
```

This will start both applications inside containers, and they will be accessible at the following URLs:

* streamlit (Frontend): `http://localhost:8501`
* FastAPI (Backend): `http://localhost:8000`