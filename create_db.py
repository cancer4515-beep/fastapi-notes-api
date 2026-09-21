from app import models
from app.database import Base, engine


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    print("Đã tạo database và các bảng thành công!")


if __name__ == "__main__":
    create_tables()