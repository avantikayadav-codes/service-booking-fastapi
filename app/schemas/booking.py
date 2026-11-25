from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime, timezone
from typing import Literal

BookingStatus = Literal["Pending", "Confirmed", "Cancelled", "Completed"]


class BookingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_id:int
    booking_date:datetime

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            current_time = datetime.now()
        else:
            current_time = datetime.now(value.tzinfo)

        if value <= current_time:
            raise ValueError("Booking date must be in the future")

        return value

class BookingResponse(BaseModel):
    id:int
    user_id:int
    service_id:int
    booking_date:datetime
    status:str

class BookingUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    booking_date: datetime | None = None
    status: BookingStatus | None = None

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value

        if value.tzinfo is None:
            current_time = datetime.now()
        else:
            current_time = datetime.now(value.tzinfo)

        if value <= current_time:
            raise ValueError("Booking date must be in the future")

        return value