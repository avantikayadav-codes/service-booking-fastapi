from sqlalchemy.orm import Session
from app.schemas.booking import BookingUpdate, BookingCreate
from app.models.booking import Booking
from app.models.service import Service
from datetime import datetime


def get_booking(booking_id:int,db:Session,user_id:int):
    return (db.query(Booking).filter(Booking.id==booking_id,Booking.user_id==user_id).first())

def get_bookings(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    status: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    booking_id: int | None = None,
):
    query = db.query(Booking).filter(Booking.user_id == user_id)

    if status is not None:
        query = query.filter(Booking.status == status)

    if date_from is not None:
        query = query.filter(Booking.booking_date >= date_from)

    if date_to is not None:
        query = query.filter(Booking.booking_date <= date_to)

    if booking_id is not None:
        query = query.filter(Booking.id == booking_id)

    return (
        query.order_by(Booking.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_booking(booking:BookingCreate,db:Session,user_id:int):
    service = db.query(Service).filter(
        Service.id == booking.service_id
    ).first()

    if service is None:
        return None
    new_booking=Booking(
        user_id=user_id,
        service_id=booking.service_id,
        booking_date=booking.booking_date
    )
    try:
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking
    except Exception:
        db.rollback()
        raise

def update_booking(booking_id:int,booking:BookingUpdate,db:Session,user_id:int,is_admin:bool=False):
    query = db.query(Booking).filter(Booking.id == booking_id)
    if not is_admin:
        query = query.filter(Booking.user_id == user_id)
    existing_booking = query.first()

    if existing_booking is None:
        return None
    if booking.booking_date is not None:
        existing_booking.booking_date=booking.booking_date
    if booking.status is not None:
        existing_booking.status=booking.status
    try:
        db.commit()
        db.refresh(existing_booking)
        return existing_booking
    except Exception:
        db.rollback()
        raise

def delete_booking(booking_id:int,db:Session,user_id:int):
    existing_booking=db.query(Booking).filter(Booking.id==booking_id, Booking.user_id == user_id).first()
    if existing_booking is None:
        return None
    try:
        db.delete(existing_booking)
        db.commit()
        return existing_booking
    except Exception:
        db.rollback()
        raise