from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from datetime import datetime
from fastapi.responses import RedirectResponse
from app.database import get_db_connection
# from app.routes import products
from pydantic import BaseModel
import hashlib
import os

salt = os.urandom(16)

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    email: str
    password: int
    created_at: int
    # role = 'user'

templates = Jinja2Templates(directory="app/templates")

@router.get("/register/")
def show_registration_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/users/")
def get_users(request: Request):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    # cur.execute("SELECT id, name FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("start.html", {"request": request, "users": users})

@router.post("/users/")
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',  
            password.encode('utf-8'),  
            salt, 
            100000,  
            dklen=32 
        )
        email = email.strip()
        email = email.lower()
        cur.execute(
            "INSERT INTO users (username, email, password_hash, salt, created_at, role) VALUES (%s, %s, %s, %s, NOW(), %s) RETURNING user_id",
            (name, email, hashed_password, salt, "user")
        )


        row = cur.fetchone()
        print("DEBUG: fetchone() output ->", row) 
        
        if not row:
            raise HTTPException(status_code=500, detail="Ошибка при создании пользователя (id не получен)")

        conn.commit()

        return RedirectResponse(url="/login/", status_code=303)

    except Exception as e:
        conn.rollback()
        import traceback
        error_details = traceback.format_exc()
        print(f"Ошибка SQL: {e}\nДетали:\n{error_details}")  
        raise HTTPException(status_code=500, detail=f"Ошибка SQL: {str(e)}")

    finally:
        cur.close()
        conn.close()

@router.post("/login/")
async def login_user(email: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        try:
            cur.execute("SELECT user_id, password_hash, salt FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
        except Exception as e:
            print(f"DEBUG: Ошибка при выполнении запроса: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при запросе к базе данных")
        
        if not user:
            raise HTTPException(status_code=400, detail="Неверный email или пароль")

        # print("данные пользователя из БД ----->", user)  

        user_id = user["user_id"]
        stored_password = user["password_hash"]
        stored_salt = user["salt"]

        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(status_code=500, detail=f"Ошибка: id={user_id} (ожидался int)")

        hashed_input_password = hashlib.pbkdf2_hmac(
            'sha256',  
            password.encode('utf-8'),  
            stored_salt, 
            100000,  
            dklen=32 
        )

        if hashed_input_password != bytes.fromhex(stored_password[2:]): 
            raise HTTPException(status_code=400, detail="Неверный email или пароль")

        # return {"message": "вход выполнен успешно", "user_id": user_id}
        return RedirectResponse(url="/home/", status_code=303) 


    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Неверный email или пароль")

    finally:
        cur.close()
        conn.close()
