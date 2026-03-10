from pydantic import ConfigDict
from sqlalchemy import Text, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class VendorComment(Base):
    __tablename__ = "vendor_comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cve_id: Mapped[str] = mapped_column(
        Text, ForeignKey("cve.id", ondelete="CASCADE")
    )

    organization: Mapped[str | None] = mapped_column(Text)
    comment: Mapped[str | None] = mapped_column(Text)
    last_modified: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))

    model_config = ConfigDict(from_attributes=True)