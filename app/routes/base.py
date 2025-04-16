from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from app.database import get_db_connection
from fastapi.responses import RedirectResponse, FileResponse
import google.generativeai as genai


genai.configure(api_key="AIzaSyC1yUKKBcQVh5eWnWt0EAYfFcusdWK9aHM")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/home/")
def home_page():
    return FileResponse("app/templates/home.html") 

@router.get("/about/")
def about_page():
    return FileResponse("app/templates/about.html") 

@router.get("/sex/")
def show_shop(request: Request):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT product_id, product_name, description, price, image FROM products")
        products = cur.fetchall()
        product_list = [
            {
                "id": row["product_id"],
                "name": row["product_name"],
                "description": row["description"] if row["description"] else "No description.",
                "price": row["price"],
                "image": row["image"]
            } for row in products
        ]
        
    finally:
        cur.close()
        conn.close()

    return templates.TemplateResponse("shop.html", {
        "request": request,
        "products": product_list,
    })
