"""create site_metrics table

Revision ID: 0003_site_metrics
Revises: 0002_users
Create Date: 2026-09-17 18:20:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0003_site_metrics"
down_revision: Union[str, None] = "0002_users"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "site_metrics",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("site_id", sa.String(length=64), nullable=False),
        sa.Column("month", sa.String(length=16), nullable=False),
        sa.Column("canopy_cover", sa.Float(), nullable=True),
        sa.Column("carbon_sequestration", sa.Float(), nullable=True),
        sa.Column("biomass_density", sa.Float(), nullable=True),
        sa.Column("biodiversity_index", sa.Float(), nullable=True),
        sa.Column("species_count", sa.Integer(), nullable=True),
        sa.Column("disturbance_index", sa.Float(), nullable=True),
        sa.Column("health_score", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["site_id"],
            ["sites.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("site_id", "month", name="uq_site_metrics_site_month"),
    )
    op.create_index(op.f("ix_site_metrics_site_id"), "site_metrics", ["site_id"], unique=False)
    op.create_index(op.f("ix_site_metrics_month"), "site_metrics", ["month"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_site_metrics_month"), table_name="site_metrics")
    op.drop_index(op.f("ix_site_metrics_site_id"), table_name="site_metrics")
    op.drop_table("site_metrics")
