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

@router.get("/stat/")
def show_shop(request: Request):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT product_id, product_name, description, price, image FROM products")
        products = cur.fetchall()

        formatted_data = "\n".join([
            f"{row[1]} — {row[3]} ₸. {row[2] or 'Нет описания'}"
            for row in products
        ])

        prompt = (
            "Сделай краткий аналитический отчёт по следующим товарам:\n"
            f"{formatted_data}\n\n"
            "Найди самый дорогой и самый дешёвый товар, сделай распределение по ценам."
        )

        response = model.generate_content(prompt)

        stat_text = response.text
        print("DEBUG: RESPONSE TEXT >>>")
        print(response.text)


    finally:
        cur.close()
        conn.close()

    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "stat": stat_text
    })

