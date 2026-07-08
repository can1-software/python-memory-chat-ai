"""add users timestamps

Revision ID: 2d882bdd012b
Revises: 3209748143cf
Create Date: 2026-07-08 11:51:03.610618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2d882bdd012b"
down_revision: Union[str, Sequence[str], None] = "3209748143cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add created_at / updated_at if missing (old create_all table)."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("users")}

    if "created_at" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
        )

    if "updated_at" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
        )


def downgrade() -> None:
    """Remove timestamp columns."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("users")}

    if "updated_at" in columns:
        op.drop_column("users", "updated_at")

    if "created_at" in columns:
        op.drop_column("users", "created_at")
