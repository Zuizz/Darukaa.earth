import uuid
from datetime import datetime
from sqlalchemy import String, Float, Integer, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class SiteMetric(Base):
    __tablename__ = "site_metrics"
    __table_args__ = (
        UniqueConstraint("site_id", "month", name="uq_site_metrics_site_month"),
    )

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        default=lambda: f"met-{uuid.uuid4().hex[:8]}",
    )
    site_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Stored as YYYY-MM (e.g. '2024-06')
    month: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    # Carbon project metrics
    canopy_cover: Mapped[float | None] = mapped_column(Float, nullable=True)
    carbon_sequestration: Mapped[float | None] = mapped_column(Float, nullable=True)
    biomass_density: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Biodiversity project metrics
    biodiversity_index: Mapped[float | None] = mapped_column(Float, nullable=True)
    species_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    disturbance_index: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Composite health score for the month
    health_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    site = relationship("Site", back_populates="metrics")
