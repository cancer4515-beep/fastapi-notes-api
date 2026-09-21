from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

    model_config = ConfigDict(extra="forbid")

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        value = value.strip().lower()

        if len(value) < 3:
            raise ValueError("Username phải có ít nhất 3 ký tự")

        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Mật khẩu không được vượt quá 72 byte")

        return value


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
class NoteCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
    )

    content: str = Field(
        min_length=1,
    )

    completed: bool = False
    due_date: datetime | None = None

    tags: list[str] = Field(
        default_factory=list,
        max_length=10,
    )

    model_config = ConfigDict(
        extra="forbid"
    )

    @field_validator(
        "title",
        "content",
    )
    @classmethod
    def fields_not_blank(
        cls,
        value: str,
    ) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Dữ liệu không được chỉ chứa khoảng trắng"
            )

        return cleaned_value

    @field_validator("tags")
    @classmethod
    def normalize_tags(
        cls,
        values: list[str],
    ) -> list[str]:
        cleaned_tags = []

        for value in values:
            tag = value.strip().lower()

            if not tag:
                continue

            if len(tag) > 30:
                raise ValueError(
                    "Mỗi tag tối đa 30 ký tự"
                )

            if tag not in cleaned_tags:
                cleaned_tags.append(tag)

        return cleaned_tags

class NoteUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    content: str | None = Field(
        default=None,
        min_length=1,
    )

    completed: bool | None = None

    due_date: datetime | None = None

    tags: list[str] | None = Field(
        default=None,
        max_length=10,
    )

    model_config = ConfigDict(
        extra="forbid"
    )

    @field_validator("title", "content")
    @classmethod
    def fields_not_blank(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Dữ liệu không được chỉ chứa khoảng trắng"
            )

        return cleaned_value


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str

    completed: bool
    due_date: datetime | None
    tags: list[str]

    owner_id: int

    model_config = ConfigDict(
        from_attributes=True
    )