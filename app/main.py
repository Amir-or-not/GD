from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import users, products, base
from fastapi.responses import FileResponse

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(users.router)
app.include_router(products.router)

@app.get("/")
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
    
@app.get("/login/")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/logout/")
def get_login_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/shop/")
def shop_page(request: Request):
    return templates.TemplateResponse("shop.html", {"request": request})

@app.get("/home/")
def home_page():
    return FileResponse("app/templates/home.html")

@app.get("/about/")
def about_page():
    return FileResponse("app/templates/about.html") 

@app.get("/product/{product_id}/")
def get_product_detail():
    return FileResponse("app/templates/product_detail.html") 


@app.get("/profile/")
def profile_page():
    return FileResponse("app/templates/profile.html")


@app.get("/analytics/")
def profile_page():
    return FileResponse("app/templates/analytics.html")


#     venv/Scripts/activate
#     uvicorn app.main:app --reload
#     uvicorn app.main:app --host 127.0.0.1 --port 8080