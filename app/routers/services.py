import shutil
import uuid
from pathlib import Path

from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query,
    UploadFile,
    File,
)

from app.database.database import get_db
from app.schemas.service import ServiceUpdate, ServiceCreate, ServiceResponse
from app.crud.service import (
    get_service,
    get_services,
    create_service,
    update_service,
    delete_service,
)
from app.core.dependencies import get_admin_user
from app.models.user import User
from PIL import Image, UnidentifiedImageError





router=APIRouter(
    prefix="/services",
    tags=["Services"]
)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB



@router.get("/{service_id}",response_model=ServiceResponse)
def read_service(service_id:int,db:Session=Depends(get_db)):
    service=get_service(service_id,db)
    if service is None:
        raise HTTPException(status_code=404,detail="Service Not found!")
    return service

@router.get("/", response_model=list[ServiceResponse])
def read_services(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    search: str | None = Query(default=None, min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=422,
            detail="min_price cannot be greater than max_price",
        )
    return get_services(
        db=db,
        skip=skip,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        search=search,
    )

@router.post("/",response_model=ServiceResponse)
def create_new_service(service:ServiceCreate,db:Session=Depends(get_db),current_user:User=Depends(get_admin_user)):
    return create_service(service,db)

@router.patch("/{service_id}",response_model=ServiceResponse)
def update_exisiting_service(service:ServiceUpdate,service_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_admin_user)):
    exist_service=update_service(service,service_id,db)
    if exist_service is None:
        raise HTTPException(status_code=404,detail="Service Not found!")
    return exist_service

@router.delete("/{service_id}")
def delete_existing_service(service_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_admin_user)):
    del_service=delete_service(service_id,db)
    if del_service is None:
        raise HTTPException(status_code=404,detail="Service Not found!")
    return {"Message":"Service is deleted Successfully!"}







@router.post("/{service_id}/upload-image", response_model=ServiceResponse)
def upload_service_image(
    service_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    service = get_service(service_id, db)

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service Not found!"
        )

    allowed_types = {
        "JPEG": ("image/jpeg", ".jpg"),
        "PNG": ("image/png", ".png"),
        "WEBP": ("image/webp", ".webp"),
    }

    temp_path = UPLOAD_DIR / f"{uuid.uuid4()}.tmp"
    final_path = None
    file_size = 0

    try:
        # 1. File size validation and temporary saving
        with temp_path.open("wb") as buffer:
            while True:
                chunk = image.file.read(1024 * 1024)

                if not chunk:
                    break

                file_size += len(chunk)

                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Image size must not exceed 5 MB!"
                    )

                buffer.write(chunk)

        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty file is not allowed!"
            )

        # 2. Validate actual image content
        try:
            with Image.open(temp_path) as img:
                image_format = img.format
                img.verify()

        except (UnidentifiedImageError, OSError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Invalid or corrupted image file!"
            )

        if image_format not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG and WEBP images are allowed!"
            )

        # 3. Validate MIME type
        expected_mime, extension = allowed_types[image_format]

        if image.content_type != expected_mime:
            raise HTTPException(
                status_code=400,
                detail="Image content type does not match its actual format!"
            )

        # 4. Generate unique filename
        unique_filename = f"{uuid.uuid4()}{extension}"
        final_path = UPLOAD_DIR / unique_filename

        temp_path.replace(final_path)

        # 5. Save image path in database
        old_image_path = service.image_path

        service.image_path = str(final_path)
        db.commit()
        db.refresh(service)

        # 6. Delete old image only after successful DB commit
        if old_image_path:
            old_path = Path(old_image_path).resolve()
            upload_directory = UPLOAD_DIR.resolve()

            if (
                old_path.is_relative_to(upload_directory)
                and old_path != final_path.resolve()
                and old_path.is_file()
            ):
                old_path.unlink()

        return service

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        if final_path and final_path.exists():
            final_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Image upload failed!"
        )

    finally:
        if temp_path.exists():
            temp_path.unlink()

        image.file.close()
