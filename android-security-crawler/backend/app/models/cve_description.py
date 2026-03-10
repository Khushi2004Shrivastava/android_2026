from pydantic import ConfigDict
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CVEDescription(Base):
    __tablename__ = "cve_description"

    cve_id: Mapped[str] = mapped_column(
        Text, ForeignKey("cve.id", ondelete="CASCADE"), primary_key=True
    )
    lang: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[str] = mapped_column(Text, primary_key=True)

    model_config = ConfigDict(from_attributes=True)