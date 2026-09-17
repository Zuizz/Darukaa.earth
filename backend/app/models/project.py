import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        default=lambda: f"prj-{uuid.uuid4().hex[:8]}",
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(64), nullable=False)  # 'carbon' | 'biodiversity'
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="active")  # 'active' | 'monitoring' | 'archived'
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    sites = relationship("Site", back_populates="project", cascade="all, delete-orphan")
