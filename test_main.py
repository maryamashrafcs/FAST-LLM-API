from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_todo():
    response = client.post(
        "/todos",
        json={"title": "Test Task", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data

def test_get_single_todo():
    # First create a task to retrieve
    post_res = client.post("/todos", json={"title": "Get Single Test", "completed": False})
    todo_id = post_res.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id

def test_update_todo():
    post_res = client.post("/todos", json={"title": "Original Title", "completed": False})
    todo_id = post_res.json()["id"]

    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "Updated Title", "completed": True}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["completed"] is True

def test_delete_todo():
    post_res = client.post("/todos", json={"title": "Task to Delete", "completed": False})
    todo_id = post_res.json()["id"]

    del_res = client.delete(f"/todos/{todo_id}")
    assert del_res.status_code == 200

    get_res = client.get(f"/todos/{todo_id}")
    assert get_res.status_code == 404