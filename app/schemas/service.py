from pydantic import BaseModel


class ServiceCreate(BaseModel):
    name: str
    description: str
    price: float


class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_path: str | None = None


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None