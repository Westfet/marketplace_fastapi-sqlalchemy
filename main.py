from fastapi import FastAPI
from routers import users
app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Marketplace API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
