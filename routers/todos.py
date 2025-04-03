from fastapi import APIRouter, Depends, Path, HTTPException, Request
from fastapi import status
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from models import Todos
from pydantic import BaseModel, Field
from .auth import get_current_user
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

templates = Jinja2Templates(directory="templates")
def redirect_to_login():
    redirect = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect.delete_cookie(key="access_token")
    return redirect


###paages###

@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        return templates.TemplateResponse("todo.html", {"request": request, "user": user,
                                                        "todos": todos})
    except:
        return redirect_to_login()

@router.get("/add-todo-page")
async def render_add_new_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})
    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, db:db_dependency, todo_id: int = Path(gt=0)):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        return templates.TemplateResponse("edit-todo.html", {"request": request, "user": user,
                                                             "todo": todo})
    except:
        return redirect_to_login()



###endpoints###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency,user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo = db.query(Todos).filter(Todos.id == todo_id,
                                  Todos.owner_id == user.get("id")).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="todo not found")
    return todo




@router.post("/todo", status_code=status.HTTP_201_CREATED)
async  def create_todo(db: db_dependency, todo_request: TodoRequest,
                       user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    new_todo = Todos(**todo_request.model_dump(), owner_id= user.get("id"))
    db.add(new_todo)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,db:db_dependency,
                      todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.get("id")).first())
    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency,user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id"))\
        .first()
    if todo is None:
        raise HTTPException(status_code=404, detail="todo not found")
    db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.get("id"))\
        .delete()
    db.commit()
