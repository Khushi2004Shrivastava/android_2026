from pydantic import ConfigDict
from sqlalchemy import Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CPEMatch(Base):
    __tablename__ = "cpe_match"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    node_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("config_node.id", ondelete="CASCADE")
    )

    vulnerable: Mapped[bool | None] = mapped_column(Boolean)
    criteria: Mapped[str | None] = mapped_column(Text)
    match_criteria_id: Mapped[str | None] = mapped_column(Text)

    version_start_excluding: Mapped[str | None] = mapped_column(Text)
    version_start_including: Mapped[str | None] = mapped_column(Text)
    version_end_excluding: Mapped[str | None] = mapped_column(Text)
    version_end_including: Mapped[str | None] = mapped_column(Text)

    model_config = ConfigDict(from_attributes=True)