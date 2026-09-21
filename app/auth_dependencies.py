from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

TokenString = Annotated[
    str,
    Depends(oauth2_scheme),
]

DatabaseSession = Annotated[
    Session,
    Depends(get_db),
]


def get_current_user(
    token: TokenString,
    db: DatabaseSession,
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        username = payload.get("sub")

        if not isinstance(username, str) or not username:
            raise credentials_exception

        token_data = schemas.TokenData(
            username=username
        )

    except InvalidTokenError as error:
        raise credentials_exception from error

    if token_data.username is None:
        raise credentials_exception

    user = crud.get_user_by_username(
        db,
        token_data.username,
    )

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị khóa",
        )

    return user