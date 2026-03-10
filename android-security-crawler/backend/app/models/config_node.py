from pydantic import ConfigDict
from sqlalchemy import Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ConfigNode(Base):
    __tablename__ = "config_node"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cve_id: Mapped[str] = mapped_column(
        Text, ForeignKey("cve.id", ondelete="CASCADE")
    )

    operator: Mapped[str | None] = mapped_column(Text)
    negate: Mapped[bool | None] = mapped_column(Boolean)
    node_index: Mapped[int | None] = mapped_column(Integer)

    cpe_matches = relationship("CPEMatch", cascade="all, delete-orphan")

    model_config = ConfigDict(from_attributes=True)