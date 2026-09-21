from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.auth_dependencies import get_current_user
from app.database import get_db


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

DatabaseSession = Annotated[
    Session,
    Depends(get_db),
]

CurrentUser = Annotated[
    models.User,
    Depends(get_current_user),
]


@router.post(
    "/",
    response_model=schemas.NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note_data: schemas.NoteCreate,
    db: DatabaseSession,
    current_user: CurrentUser,
):
    return crud.create_note(
        db=db,
        note_data=note_data,
        owner_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[schemas.NoteResponse],
)
def read_my_notes(
    db: DatabaseSession,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
):
    return crud.get_notes_by_owner(
        db=db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
        search=search,
    )


@router.get(
    "/{note_id}",
    response_model=schemas.NoteResponse,
)
def read_my_note(
    note_id: int,
    db: DatabaseSession,
    current_user: CurrentUser,
):
    note = crud.get_note_by_id_and_owner(
        db=db,
        note_id=note_id,
        owner_id=current_user.id,
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy note",
        )

    return note


@router.put(
    "/{note_id}",
    response_model=schemas.NoteResponse,
)
def update_my_note(
    note_id: int,
    note_data: schemas.NoteUpdate,
    db: DatabaseSession,
    current_user: CurrentUser,
):
    note = crud.get_note_by_id_and_owner(
        db=db,
        note_id=note_id,
        owner_id=current_user.id,
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy note",
        )

    return crud.update_note(
        db=db,
        note=note,
        note_data=note_data,
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_note(
    note_id: int,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> None:
    note = crud.get_note_by_id_and_owner(
        db=db,
        note_id=note_id,
        owner_id=current_user.id,
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy note",
        )

    crud.delete_note(db=db, note=note)