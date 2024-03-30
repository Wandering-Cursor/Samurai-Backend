"""Nullable reviewer

Revision ID: 1c0a97691b8d
Revises: 07e6a40068a8
Create Date: 2024-03-30 16:40:35.634074

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1c0a97691b8d"
down_revision = "07e6a40068a8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("taskmodel", "reviewer", existing_type=sa.UUID(), nullable=True)
    op.alter_column("usertaskmodel", "reviewer", existing_type=sa.UUID(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("usertaskmodel", "reviewer", existing_type=sa.UUID(), nullable=False)
    op.alter_column("taskmodel", "reviewer", existing_type=sa.UUID(), nullable=False)
    # ### end Alembic commands ###
