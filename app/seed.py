from app.database.database import SessionLocal
from app.core.config import settings
from app.core.security import password_hash
from app.models.user import User


def seed_super_admin():
    if not settings.ADMIN_EMAIL or not settings.ADMIN_PASSWORD:
        print("ADMIN_EMAIL / ADMIN_PASSWORD not set, skipping seed")
        return

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if existing:
            print("Super admin already exists, skipping")
            return

        db.add(User(
            name="Super Admin",
            email=settings.ADMIN_EMAIL,
            password=password_hash(settings.ADMIN_PASSWORD),
            role="super_admin",
        ))
        db.commit()
        print("Super admin created")
    finally:
        db.close()


if __name__ == "__main__":
    seed_super_admin()