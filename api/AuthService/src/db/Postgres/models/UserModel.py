from sqlalchemy import Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from db.Postgres.Base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(Uuid, unique=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)

    def as_dict(self)->dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}