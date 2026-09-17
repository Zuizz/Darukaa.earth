"""create projects and sites tables

Revision ID: 0001_initial
Revises: 
Create Date: 2026-09-17 17:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import geoalchemy2

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ensure PostGIS extension is available
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "projects",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="active"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "sites",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("project_id", sa.String(length=64), nullable=False),
        sa.Column("site_type", sa.String(length=64), nullable=True),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(
                geometry_type="POLYGON",
                srid=4326,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                spatial_index=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(op.f("ix_sites_project_id"), "sites", ["project_id"], unique=False)
    op.create_index(
        "idx_sites_geometry",
        "sites",
        ["geometry"],
        unique=False,
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index("idx_sites_geometry", table_name="sites", postgresql_using="gist")
    op.drop_index(op.f("ix_sites_project_id"), table_name="sites")
    op.drop_table("sites")
    op.drop_table("projects")
