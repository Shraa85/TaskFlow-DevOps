import os
import tempfile
import pytest
import gc

@pytest.fixture()
def client(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    monkeypatch.setenv("TASKFLOW_DB", path)
    import app as taskflow
    taskflow.DATABASE = path
    taskflow.init_db()
    taskflow.app.config["TESTING"] = True
    with taskflow.app.test_client() as client:
        yield client
        
    gc.collect()
    try:
        os.unlink(path)
    except PermissionError:
        pass

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskFlow" in response.data

def test_add_task_and_api(client):
    response = client.post("/tasks", data={"title": "Submit lab report", "description": "Finish before deadline"})
    assert response.status_code == 302
    tasks = client.get("/api/tasks").get_json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Submit lab report"

def test_toggle_and_delete_task(client):
    client.post("/tasks", data={"title": "Test task"})
    task_id = client.get("/api/tasks").get_json()[0]["id"]
    client.post(f"/tasks/{task_id}/toggle")
    assert client.get("/api/tasks").get_json()[0]["completed"] == 1
    client.post(f"/tasks/{task_id}/delete")
    assert client.get("/api/tasks").get_json() == []

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
