from fastapi import APIRouter,HTTPException,Depends,Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.booking import BookingResponse,BookingUpdate,BookingCreate
from app.crud.booking import get_booking,get_bookings,create_booking,update_booking,delete_booking
from app.core.dependencies import get_current_user
from app.models.user import User
from typing import Literal
from datetime import datetime
from app.tasks import send_booking_email


router=APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)



@router.get("/{booking_id}",response_model=BookingResponse)
def view_booking(booking_id:int,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    booking=get_booking(booking_id,db,current_user.id)
    if booking is None:
        raise HTTPException(status_code=404,detail="Booking Not Found!")
    return booking

@router.get("/", response_model=list[BookingResponse])
def view_bookings(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    status_filter: Literal[
        "Pending", "Confirmed", "Cancelled", "Completed"
    ] | None = Query(default=None, alias="status"),
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    booking_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if (
        date_from is not None
        and date_to is not None
        and date_from > date_to
    ):
        raise HTTPException(
            status_code=422,
            detail="date_from cannot be later than date_to",
        )

    return get_bookings(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status_filter,
        date_from=date_from,
        date_to=date_to,
        booking_id=booking_id,
    )


@router.post("/", response_model=BookingResponse)
def create_new_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_booking = create_booking(booking, db, current_user.id)
    if new_booking is None:
        raise HTTPException(
            status_code=404,
            detail="Service Not Found!"
        )
    try:
        send_booking_email.delay(current_user.email, new_booking.id)
    except Exception as e:
        print(f"Email task queue failed: {e}")

    return new_booking


@router.patch("/{booking_id}",response_model=BookingResponse)
def update_existing_booking(booking_id:int,booking:BookingUpdate,db:Session=Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    is_admin = current_user.role in ("admin", "super_admin")
    if not is_admin and booking.status is not None:
        if booking.status!="Cancelled":
            raise HTTPException(
                status_code=403,
                detail="Users can only cancel their own bookings"
            )
    exist_booking=update_booking(booking_id,booking,db, current_user.id,is_admin=is_admin)
    if exist_booking is None:
        raise HTTPException(status_code=404,detail="Booking Not Found!")
    return exist_booking


@router.delete("/{booking_id}")
def delete_existing_booking(booking_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    exist_booking=delete_booking(booking_id,db, current_user.id)
    if exist_booking is None:
        raise HTTPException(status_code=404,detail="Booking Not Found!")
    return {"Message":"Booking is Deleted Successfully!"}