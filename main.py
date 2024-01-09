# uvicorn main:app --host 0.0.0.0 --port 8021 --reload
import uuid
import uvicorn

from fastapi import FastAPI, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session

from datetime import datetime

from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

from fastapi import File, UploadFile

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()
IMAGEDIR = "media/"

currentlydate = datetime.now()

app.mount("/stat", StaticFiles(directory="stat"), name="stat")

@app.get("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}


def remove_files(path: str) -> None:
    os.unlink(path)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("index.html",
                                      {"request": request, "todo_list": todos})


@app.post("/add")
def addtitle(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    currentlydate = datetime.now()
    new_todo = models.Todo(title=title, date=currentlydate)
    db.add(new_todo)
    db.commit()



    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/update/{todo_id}")
def update(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.get("/delete/{todo_id}")
def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "stat", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


@app.get('/apple-touch-icon.png')
async def favicon():
    file_name = "apple-touch-icon.png"
    file_path = os.path.join(app.root_path, "stat", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


@app.get('/apple-touch-icon-precomposed.png')
async def favicon():
    file_name = "apple-touch-icon-precomposed.png"
    file_path = os.path.join(app.root_path, "stat", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})

@app.get('/apple-touch-icon-120x120-precomposed.png')
async def favicon():
    file_name = "apple-touch-icon-120x120-precomposed.png"
    file_path = os.path.join(app.root_path, "stat", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})

@app.get('/apple-touch-icon-120x120.png')
async def favicon():
    file_name = "apple-touch-icon-120x120.png"
    file_path = os.path.join(app.root_path, "stat", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.70", port=8021)