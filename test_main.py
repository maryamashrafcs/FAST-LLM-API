import pytest
from fastapi.testclient import TestClient
from main import app, todos, todo_id_counter

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    global todos, todo_id_counter
    todos.clear()
    todo_id_counter = 1

def test_create_todo():
    response = client.post("/todos", json={"title": "Test Todo", "description": "Test Desc"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Todo"

def test_get_all_todos():
    client.post("/todos", json={"title": "Todo 1"})
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_todo_by_id():
    post_response = client.post("/todos", json={"title": "Todo 1"})
    print("POST Response JSON:", post_response.json())  # Print what ID was assigned
    
    created_id = post_response.json().get("id")
    response = client.get(f"/todos/{created_id}")
    assert response.status_code == 200

def test_update_todo():
    create_res = client.post("/todos", json={"title": "Old Title"})
    created_id = create_res.json()["id"]
    
    response = client.put(f"/todos/{created_id}", json={"title": "New Title", "completed": True})
    
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
  

def test_delete_todo():
    #Create a todo and get its assigned ID
    create_res = client.post("/todos", json={"title": "Todo to Delete"})
    created_id = create_res.json()["id"]
    
    response = client.delete(f"/todos/{created_id}")
    assert response.status_code == 200
    
    assert client.get(f"/todos/{created_id}").status_code == 404