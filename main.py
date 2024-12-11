from fastapi import FastAPI
from routers import Post, User


app = FastAPI(debug=True)


# Главная страница
@app.get("/")
async def home() -> dict:
    return {"message": "My blog"}


app.include_router(Post.router)
app.include_router(User.router)

if __name__=="__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
