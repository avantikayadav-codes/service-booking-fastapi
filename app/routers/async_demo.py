import asyncio

from fastapi import APIRouter

router = APIRouter(
    prefix="/async-demo",
    tags=["Async Demo"]
)


@router.get("/")
async def async_example():
    await asyncio.sleep(2)

    return {
        "message": "Async endpoint completed",
        "concept": "await allows other async tasks to run during I/O wait"
    }