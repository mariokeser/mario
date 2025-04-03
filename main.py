from fastapi import  FastAPI, status
from models import Base
from database import engine
from routers import todos, auth, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)


@app.get("/healthy")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def home_page_todo_page():
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


