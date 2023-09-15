from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from .models import User, Content
from .security import authenticate_user, create_access_token, get_current_active_user

app = FastAPI()

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/users")
async def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.get("/users")
async def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        return user

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        db_user.username = user.username
        db_user.hashed_password = user.hashed_password
        session.commit()
        session.refresh(db_user)
        return db_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
        return {"message": "User deleted"}

@app.post("/content")
async def create_content(content: Content):
    with Session(engine) as session:
        session.add(content)
        session.commit()
        session.refresh(content)
        return content

@app.get("/content")
async def read_content():
    with Session(engine) as session:
        contents = session.exec(select(Content)).all()
        return contents

@app.get("/content/{content_id}")
async def read_content(content_id: int):
    with Session(engine) as session:
        content = session.get(Content, content_id)
        return content

@app.put("/content/{content_id}")
async def update_content(content_id: int, content: Content):
    with Session(engine) as session:
        db_content = session.get(Content, content_id)
        db_content.title = content.title
        db_content.body = content.body
        session.commit()
        session.refresh(db_content)
        return db_content

@app.delete("/content/{content_id}")
async def delete_content(content_id: int):
    with Session(engine) as session:
        content = session.get(Content, content_id)
        session.delete(content)
        session.commit()
        return {"message": "Content deleted"}
