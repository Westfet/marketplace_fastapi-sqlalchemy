import uvicorn
from fastapi import FastAPI
from routers import users_router, orders_router
from rabbit.consumers import start_consumers
from rabbit.rabbitmq import rabbitmq
from asyncio import create_task
from config import setup_logging

setup_logging()
app = FastAPI()

app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(orders_router.router, prefix="/orders", tags=["orders"])


@app.on_event("startup")
async def startup_event():
    await rabbitmq.connect()
    # Запускаем потребителей RabbitMQ в фоновом режиме
    create_task(start_consumers())


@app.on_event("shutdown")
async def shutdown_event():
    # Закрываем соединение с RabbitMQ
    await rabbitmq.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Marketplace API"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
