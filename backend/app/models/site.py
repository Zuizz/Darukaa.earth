import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from app.models.base import Base


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        default=lambda: f"site-{uuid.uuid4().hex[:8]}",
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    site_type: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # PostGIS Polygon geometry with WGS84 spatial reference (SRID 4326)
    geometry: Mapped[object] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    project = relationship("Project", back_populates="sites")
    metrics = relationship(
        "SiteMetric",
        back_populates="site",
        cascade="all, delete-orphan",
        order_by="SiteMetric.month",
    )
