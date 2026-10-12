"""Create demo accounts that match seed_data.sql voter names."""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import User
from app.security import hash_password

DEMO_USERS = [
    {
        "email": "admin@community.local",
        "display_name": "Community Admin",
        "password": "admin1234",
        "role": "admin",
    },
    {
        "email": "amina@community.local",
        "display_name": "Amina Shah",
        "password": "voter1234",
        "role": "user",
    },
    {
        "email": "leo@community.local",
        "display_name": "Leo Martins",
        "password": "voter1234",
        "role": "user",
    },
    {
        "email": "priya@community.local",
        "display_name": "Priya Nair",
        "password": "voter1234",
        "role": "user",
    },
    {
        "email": "chris@community.local",
        "display_name": "Chris Adeyemi",
        "password": "voter1234",
        "role": "user",
    },
]


def seed_demo_users() -> None:
    db = SessionLocal()
    try:
        for row in DEMO_USERS:
            exists = db.scalar(select(User.id).where(User.email == row["email"]))
            if exists:
                continue
            db.add(
                User(
                    email=row["email"],
                    display_name=row["display_name"],
                    password_hash=hash_password(row["password"]),
                    role=row["role"],
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_users()
    print("Demo users ready.")
