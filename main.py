from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sharp-Sharp 2do")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Todo(BaseModel):
    id: int
    title: str
    completed: bool=False

todos: List[Todo] = []
next_id = 1

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    global next_id
    new_todo = Todo(
        id=next_id,
        title=todo.title,
        completed=False
    )
    todos.append(new_todo)
    next_id += 1
    return new_todo

class UpdateTodo(BaseModel):
    completed: bool
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, update: UpdateTodo):
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = update.completed
            return todo
    raise HTTPException(status_code=404, detail="Can't find task")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[i]
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Can't find task")