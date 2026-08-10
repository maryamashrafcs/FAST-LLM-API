from fastapi import FastAPI, HTTPException
from models import Todo, TodoCreate
from database import init_db

app = FastAPI()

init_db()

todos: list[Todo] = []
todo_id_counter = 1

@app.get("/todos")
def get_all_todos():
    return todos

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    global todo_id_counter
    new_todo = Todo(
        id=todo_id_counter,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    todo_id_counter += 1
    todos.append(new_todo)
    return new_todo

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoCreate):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = Todo(
                id=todo_id,
                title=updated_todo.title,
                description=updated_todo.description,
                completed=updated_todo.completed
            )
            return todos[index]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")