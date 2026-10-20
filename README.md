# TaskFlow — DevOps Mini-Project

TaskFlow is a working task manager built with Flask and SQLite. It supports creating tasks, listing saved tasks, marking tasks complete/pending, and deleting tasks.

## Features
- Persistent SQLite storage
- Responsive web UI
- JSON endpoint: `/api/tasks`
- Health check endpoint: `/health`
- Automated tests with pytest
- Dockerfile and Jenkins pipeline

## Run locally (Windows)
```cmd
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```
Open http://127.0.0.1:5000

## Run tests
```cmd
py -m pytest -q
```

## Run with Docker
```cmd
docker build -t taskflow:latest .
docker run --name taskflow-app -p 5000:5000 -v taskflow-data:/data taskflow:latest
```
Open http://localhost:5000

Health check: http://localhost:5000/health
Tasks API: http://localhost:5000/api/tasks

## DevOps flow
Git/GitHub → Jenkins checkout → dependency installation → pytest → Docker image build. Configure Jenkins with a Windows agent and Docker access before running the pipeline.
