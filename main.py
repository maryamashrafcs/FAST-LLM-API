from fastapi import FastAPI, HTTPException, status
from database import init_db, get_db_connection
from models import TodoCreate

app = FastAPI()

init_db()

def row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"])
    }

# Read Endpoints (SQL SELECT)

@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [row_to_dict(row) for row in rows]

@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def get_todo(todo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    
    return row_to_dict(row)

#Placeholders!!!

@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    # We will write the SQL INSERT here in Stage 2
    pass

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: TodoCreate):
    # We will write the SQL UPDATE here in Stage 3
    pass

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    # We will write the SQL DELETE here in Stage 3
    pass