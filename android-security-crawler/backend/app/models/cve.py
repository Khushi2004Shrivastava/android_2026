from pydantic import ConfigDict
from sqlalchemy import (
    Text, Integer, Boolean, Date, TIMESTAMP, ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CVE(Base):
    __tablename__ = "cve"

    id: Mapped[str] = mapped_column(Text, primary_key=True)

    source_identifier: Mapped[str | None] = mapped_column(Text)
    vuln_status: Mapped[str | None] = mapped_column(Text)

    published: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))
    last_modified: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))

    evaluator_comment: Mapped[str | None] = mapped_column(Text)
    evaluator_solution: Mapped[str | None] = mapped_column(Text)
    evaluator_impact: Mapped[str | None] = mapped_column(Text)

    cisa_exploit_add: Mapped[str | None] = mapped_column(Date)
    cisa_action_due: Mapped[str | None] = mapped_column(Date)
    cisa_required_action: Mapped[str | None] = mapped_column(Text)
    cisa_vulnerability_name: Mapped[str | None] = mapped_column(Text)

    results_per_page: Mapped[int | None] = mapped_column(Integer)
    start_index: Mapped[int | None] = mapped_column(Integer)
    total_results: Mapped[int | None] = mapped_column(Integer)

    format: Mapped[str | None] = mapped_column(Text)
    version: Mapped[str | None] = mapped_column(Text)
    timestamp: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))

    cve_raw: Mapped[dict | None] = mapped_column(JSONB)
    processed: Mapped[bool] = mapped_column(Boolean)

    # Relationships
    descriptions = relationship("CVEDescription", cascade="all, delete-orphan")
    references = relationship("CVEReference", cascade="all, delete-orphan")
    tags = relationship("CVETag", cascade="all, delete-orphan")
    weaknesses = relationship("Weakness", cascade="all, delete-orphan")
    vendor_comments = relationship("VendorComment", cascade="all, delete-orphan")
    metrics = relationship("CVSSMetric", cascade="all, delete-orphan")
    config_nodes = relationship("ConfigNode", cascade="all, delete-orphan")

    model_config = ConfigDict(from_attributes=True)