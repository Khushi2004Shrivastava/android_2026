from pydantic import ConfigDict
from sqlalchemy import Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CVSSMetric(Base):
    __tablename__ = "cvss_metric"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cve_id: Mapped[str] = mapped_column(
        Text, ForeignKey("cve.id", ondelete="CASCADE")
    )

    version: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(Text)
    metric_type: Mapped[str | None] = mapped_column(Text)

    cvss_json: Mapped[dict | None] = mapped_column(JSONB)

    model_config = ConfigDict(from_attributes=True)