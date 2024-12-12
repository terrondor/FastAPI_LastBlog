from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import Post, User
from templates import templates



app = FastAPI(debug=True)

app.include_router(User.router)
app.include_router(Post.router)


# Главная страница
@app.get("/")
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/register")
async def register(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("register.html", {"request": request})


app.include_router(User.router)


@app.get("/login")
async def login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("login.html", {"request": request})





if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
