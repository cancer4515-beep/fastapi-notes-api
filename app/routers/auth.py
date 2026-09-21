from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

from fastapi.security import OAuth2PasswordRequestForm
from app.security import create_access_token
from app.auth_dependencies import get_current_user
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[
    models.User,
    Depends(get_current_user),
]

@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: schemas.UserRegister,
    db: DatabaseSession,
):
    if crud.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username đã tồn tại",
        )

    if crud.get_user_by_email(db, str(user_data.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email đã tồn tại",
        )

    try:
        return crud.create_user(db, user_data)
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username hoặc email đã tồn tại",
        ) from error
@router.post(
    "/login",
    response_model=schemas.Token,
)
def login_user(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    db: DatabaseSession,
) -> schemas.Token:
    user = crud.authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
    )
@router.get(
    "/me",
    response_model=schemas.UserResponse,
)
def read_current_user(
    current_user: CurrentUser,
):
    return current_user