from datetime import datetime
from sqlalchemy import DateTime, func
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
    laptime: Mapped[int]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "driver": self.driver,
            "map": self.map,
            "car": self.car,
            "laptime": self.time,
            "date": self.date
        }