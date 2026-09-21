from datetime import (
    datetime,
    timedelta,
    timezone,
)

from app import crud, schemas
from app.database import (
    Base,
    SessionLocal,
    engine,
)


def seed() -> None:

    Base.metadata.create_all(
        bind=engine
    )

    db = SessionLocal()

    try:
        user = crud.get_user_by_username(
            db,
            "demo",
        )

        if user is None:
            user = crud.create_user(
                db,
                schemas.UserRegister(
                    username="demo",
                    email="demo@example.com",
                    password="matkhau123",
                ),
            )

        existing_notes = (
            crud.get_notes_by_owner(
                db=db,
                owner_id=user.id,
                limit=100,
            )
        )

        if existing_notes:
            print(
                "Seed đã tồn tại, bỏ qua."
            )
            return

        crud.create_note(
            db=db,
            owner_id=user.id,
            note_data=schemas.NoteCreate(
                title="Học FastAPI",
                content="Hoàn thành Day 51",
                tags=[
                    "python",
                    "fastapi",
                ],
                due_date=(
                    datetime.now(
                        timezone.utc
                    )
                    + timedelta(days=3)
                ),
            ),
        )

        crud.create_note(
            db=db,
            owner_id=user.id,
            note_data=schemas.NoteCreate(
                title="Ôn SQL",
                content="Ôn JOIN và GROUP BY",
                tags=[
                    "sql",
                    "database",
                ],
            ),
        )

        print(
            "Seed data thành công!"
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed()