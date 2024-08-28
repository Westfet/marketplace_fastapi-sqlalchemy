from fastapi import APIRouter
from controllers.orders_controller import OrderCreate, OrderResponse, rabbitmq_order_worker, get_order


router = APIRouter()


@router.post("/")
async def create_order_view(order: OrderCreate):
    await rabbitmq_order_worker(order)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_view(order_id: int):
    db_order = await get_order(order_id)
    return OrderResponse(
        id=db_order.id,
        user_id=db_order.user_id,
        status=db_order.status
    )
