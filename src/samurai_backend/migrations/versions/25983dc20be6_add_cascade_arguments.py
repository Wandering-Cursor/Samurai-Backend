"""Add cascade arguments

Revision ID: 25983dc20be6
Revises: e966c95d7210
Create Date: 2024-05-20 17:40:52.964379

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "25983dc20be6"
down_revision = "e966c95d7210"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("userprojectlinkmodel", "account_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column(
        "userprojectlinkmodel", "user_project_id", existing_type=sa.UUID(), nullable=True
    )
    op.create_index(
        op.f("ix_userprojectlinkmodel_account_id"),
        "userprojectlinkmodel",
        ["account_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_userprojectlinkmodel_user_project_id"),
        "userprojectlinkmodel",
        ["user_project_id"],
        unique=False,
    )
    op.drop_constraint(
        "userprojectlinkmodel_user_project_id_fkey", "userprojectlinkmodel", type_="foreignkey"
    )
    op.drop_constraint(
        "userprojectlinkmodel_account_id_fkey", "userprojectlinkmodel", type_="foreignkey"
    )
    op.create_foreign_key(
        None,
        "userprojectlinkmodel",
        "accountmodel",
        ["account_id"],
        ["account_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None,
        "userprojectlinkmodel",
        "userprojectmodel",
        ["user_project_id"],
        ["project_id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "userprojectlinkmodel", type_="foreignkey")
    op.drop_constraint(None, "userprojectlinkmodel", type_="foreignkey")
    op.create_foreign_key(
        "userprojectlinkmodel_account_id_fkey",
        "userprojectlinkmodel",
        "accountmodel",
        ["account_id"],
        ["account_id"],
    )
    op.create_foreign_key(
        "userprojectlinkmodel_user_project_id_fkey",
        "userprojectlinkmodel",
        "userprojectmodel",
        ["user_project_id"],
        ["project_id"],
    )
    op.drop_index(
        op.f("ix_userprojectlinkmodel_user_project_id"), table_name="userprojectlinkmodel"
    )
    op.drop_index(op.f("ix_userprojectlinkmodel_account_id"), table_name="userprojectlinkmodel")
    op.alter_column(
        "userprojectlinkmodel", "user_project_id", existing_type=sa.UUID(), nullable=False
    )
    op.alter_column("userprojectlinkmodel", "account_id", existing_type=sa.UUID(), nullable=False)
    # ### end Alembic commands ###
