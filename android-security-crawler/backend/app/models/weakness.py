from pydantic import ConfigDict
from sqlalchemy import Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Weakness(Base):
    __tablename__ = "weakness"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cve_id: Mapped[str] = mapped_column(
        Text, ForeignKey("cve.id", ondelete="CASCADE")
    )

    source: Mapped[str | None] = mapped_column(Text)
    type: Mapped[str | None] = mapped_column(Text)
    lang: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)

    model_config = ConfigDict(from_attributes=True)