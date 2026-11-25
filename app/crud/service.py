from sqlalchemy.orm import Session
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.models.service import Service


def get_service(service_id: int, db: Session):
    return (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )


def get_services(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
):
    query = db.query(Service)

    if min_price is not None:
        query = query.filter(Service.price >= min_price)

    if max_price is not None:
        query = query.filter(Service.price <= max_price)

    if search:
        query = query.filter(Service.name.ilike(f"%{search}%"))

    return (
        query.order_by(Service.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_service(service: ServiceCreate, db: Session):
    new_service = Service(
        name=service.name,
        description=service.description,
        price=service.price,
    )

    try:
        db.add(new_service)
        db.commit()
        db.refresh(new_service)
        return new_service
    except Exception:
        db.rollback()
        raise


def update_service(
    service: ServiceUpdate,
    service_id: int,
    db: Session,
):
    exist_service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if exist_service is None:
        return None

    if service.name is not None:
        exist_service.name = service.name

    if service.description is not None:
        exist_service.description = service.description

    if service.price is not None:
        exist_service.price = service.price

    try:
        db.commit()
        db.refresh(exist_service)
        return exist_service
    except Exception:
        db.rollback()
        raise


def delete_service(service_id: int, db: Session):
    exist_service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if exist_service is None:
        return None

    try:
        db.delete(exist_service)
        db.commit()
        return exist_service
    except Exception:
        db.rollback()
        raise
