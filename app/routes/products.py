from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from app.database import get_db_connection
from fastapi.responses import RedirectResponse
from app.routes import users, products, base
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

@router.get("/cart/")
def show_cart(request: Request):
    conn = get_db_connection()
    cur = conn.cursor()
    
    user_id = request.cookies.get("user_id")
    
    # if not user_id:
    #     return RedirectResponse(url="/login/")  

    try:
        cur.execute("""
            select p.product_id, p.product_name, p.description, p.image, p.price, c.quantity
            from cart c
            join products p on c.product_id = p.product_id
            where c.user_id = %s
        """, (user_id,))
        
        cart_items = cur.fetchall()

        items = [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2] or "Нет описания",
                "image": row[3],
                "price": row[4],
                "quantity": row[5]
            } for row in cart_items
        ]

    finally:
        cur.close()
        conn.close()

    return templates.TemplateResponse("cart-bag.html", {
        "request": request,
        "items": items
    })

@router.post("/add-to-cart/{product_id}")
def add_to_cart(request: Request, product_id: int, quantity: int = Form(1)):
    conn = get_db_connection()
    cur = conn.cursor()

    user_id = request.cookies.get("user_id") or 1

    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        cur.execute("""
            select quantity from cart
            where user_id = %s and product_id = %s
        """, (user_id, product_id))
        result = cur.fetchone()

        if result:
            cur.execute("""
                update cart
                set quantity = quantity + %s
                where user_id = %s and product_id = %s
            """, (quantity, user_id, product_id))
        else:
            cur.execute("""
                insert into cart (user_id, product_id, quantity)
                values (%s, %s, %s)
            """, (user_id, product_id, quantity))

        conn.commit()
    finally:
        cur.close()
        conn.close()

    return RedirectResponse(url="/shop/", status_code=302)  

@router.post("/admin/add-product/")
def add_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    old_price: float = Form(...),
    new_price: float = Form(...),
    image_url: str = Form(...)
):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO products (name, description, old_price, new_price, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, old_price, new_price, image_url))
        conn.commit()
    finally:
        cur.close()
        conn.close()

    return RedirectResponse(url="/shop/", status_code=303)