from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.security import hash_password, verify_password

DUMMY_HASH = hash_password("dummy-password")
def get_user_by_username(
    db: Session,
    username: str,
) -> models.User | None:
    statement = select(models.User).where(
        models.User.username == username
    )
    return db.scalar(statement)


def get_user_by_email(
    db: Session,
    email: str,
) -> models.User | None:
    statement = select(models.User).where(
        models.User.email == email
    )
    return db.scalar(statement)


def create_user(
    db: Session,
    user_data: schemas.UserRegister,
) -> models.User:
    new_user = models.User(
        username=user_data.username,
        email=str(user_data.email),
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(new_user)
    return new_user
def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> models.User | None:
    normalized_username = username.strip().lower()

    user = get_user_by_username(
        db,
        normalized_username,
    )

    if user is None:
        # Vẫn chạy bcrypt để hạn chế dò username
        verify_password(password, DUMMY_HASH)
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    if not user.is_active:
        return None

    return user
def create_note(
    db: Session,
    note_data: schemas.NoteCreate,
    owner_id: int,
) -> models.Note:
    new_note = models.Note(
        title=note_data.title,
        content=note_data.content,
        owner_id=owner_id,
    )

    db.add(new_note)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(new_note)
    return new_note


def get_notes_by_owner(
    db: Session,
    owner_id: int,
) -> list[models.Note]:
    statement = (
        select(models.Note)
        .where(models.Note.owner_id == owner_id)
        .order_by(models.Note.id)
    )

    return list(db.scalars(statement).all())


def get_note_by_id_and_owner(
    db: Session,
    note_id: int,
    owner_id: int,
) -> models.Note | None:
    statement = select(models.Note).where(
        models.Note.id == note_id,
        models.Note.owner_id == owner_id,
    )

    return db.scalar(statement)


def update_note(
    db: Session,
    note: models.Note,
    note_data: schemas.NoteUpdate,
) -> models.Note:
    update_data = note_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for field, value in update_data.items():
        setattr(note, field, value)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(note)
    return note


def delete_note(
    db: Session,
    note: models.Note,
) -> None:
    db.delete(note)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise