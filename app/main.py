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
    pass

@app.get("/users")
async def read_users():
    pass

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    pass

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    pass

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    pass

@app.post("/content")
async def create_content(content: Content):
    pass

@app.get("/content")
async def read_content():
    pass

@app.get("/content/{content_id}")
async def read_content(content_id: int):
    pass

@app.put("/content/{content_id}")
async def update_content(content_id: int, content: Content):
    pass

@app.delete("/content/{content_id}")
async def delete_content(content_id: int):
    pass
