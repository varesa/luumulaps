from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class LapTime(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    driver: Mapped[str]
    map: Mapped[str]
    car: Mapped[str]
    time: Mapped[int]