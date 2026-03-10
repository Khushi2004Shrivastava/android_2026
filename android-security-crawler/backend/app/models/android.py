from pydantic import ConfigDict
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class Android(Base):
    __tablename__ = "android"

    id: Mapped[str] = mapped_column(primary_key=True)

    model_config = ConfigDict(from_attributes=True)