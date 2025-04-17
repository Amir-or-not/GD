from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from app.database import get_db_connection
from fastapi.responses import RedirectResponse
import google.generativeai as genai


genai.configure(api_key="AIzaSyC1yUKKBcQVh5eWnWt0EAYfFcusdWK9aHM")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/shop/")
def show_shop(request: Request):
    conn = get_db_connection()
    cur = conn.cursor()
    role = request.cookies.get("role", "user")
    try:
        cur.execute("SELECT product_id, product_name, description, price, image FROM products")
        products = cur.fetchall()
        # print("DEBUG: products from DB -->", products)
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
        "role": role
    })


@router.get("/product/{product_name}/")
def product_detail(product_name: str, request: Request):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT product_id, product_name, description, price, image FROM products WHERE product_name = %s", (product_name,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")

        product = {
            "id": row["product_id"],
            "name": row["product_name"],
            "description": row["description"] if row["description"] else "No description.",
            "price": row["price"],
            "image_url": row["image"]
        }
    finally:
        cur.close()
        conn.close()

    return templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": product
    })

# @router.post("/admin/add-product/")
# def add_product(
#     request: Request,
#     name: str = Form(...),
#     description: str = Form(...),
#     old_price: float = Form(...),
#     new_price: float = Form(...),
#     image_url: str = Form(...)
# ):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO products (name, description, old_price, new_price, image_url)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (name, description, old_price, new_price, image_url))
#         conn.commit()
#     finally:
#         cur.close()
#         conn.close()

#     return RedirectResponse(url="/shop/", status_code=303)