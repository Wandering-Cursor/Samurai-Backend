"""Update Files

Revision ID: a1b85513c68b
Revises: e24ff83b92a7
Create Date: 2024-05-15 21:51:01.038343

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "a1b85513c68b"
down_revision = "e24ff83b92a7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "filemodel", sa.Column("uploaded_by_id", sqlmodel.sql.sqltypes.GUID(), nullable=False)
    )
    op.create_foreign_key(None, "filemodel", "accountmodel", ["uploaded_by_id"], ["account_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "filemodel", type_="foreignkey")
    op.drop_column("filemodel", "uploaded_by_id")
    # ### end Alembic commands ###