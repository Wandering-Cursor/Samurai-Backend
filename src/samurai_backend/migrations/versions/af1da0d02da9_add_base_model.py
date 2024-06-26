"""Add Base Model

Revision ID: af1da0d02da9
Revises: 13b56ccfb196
Create Date: 2024-04-03 20:08:32.374022

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "af1da0d02da9"
down_revision = "13b56ccfb196"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accountmodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "accountmodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "accountpermission", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "accountpermission", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "accountpermissionaccountlink",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "accountpermissionaccountlink",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "connectionlinkmodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "connectionlinkmodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "connectionmodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "connectionmodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "departmentmodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "departmentmodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "facultymodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "facultymodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("groupmodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("groupmodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(
        "projectmodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "projectmodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "registrationemailcode", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "registrationemailcode", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("taskmodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("taskmodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(
        "userprojectmodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "userprojectmodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "usertaskmodel", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "usertaskmodel", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("usertaskmodel", "updated_at")
    op.drop_column("usertaskmodel", "created_at")
    op.drop_column("userprojectmodel", "updated_at")
    op.drop_column("userprojectmodel", "created_at")
    op.drop_column("taskmodel", "updated_at")
    op.drop_column("taskmodel", "created_at")
    op.drop_column("registrationemailcode", "updated_at")
    op.drop_column("registrationemailcode", "created_at")
    op.drop_column("projectmodel", "updated_at")
    op.drop_column("projectmodel", "created_at")
    op.drop_column("groupmodel", "updated_at")
    op.drop_column("groupmodel", "created_at")
    op.drop_column("facultymodel", "updated_at")
    op.drop_column("facultymodel", "created_at")
    op.drop_column("departmentmodel", "updated_at")
    op.drop_column("departmentmodel", "created_at")
    op.drop_column("connectionmodel", "updated_at")
    op.drop_column("connectionmodel", "created_at")
    op.drop_column("connectionlinkmodel", "updated_at")
    op.drop_column("connectionlinkmodel", "created_at")
    op.drop_column("accountpermissionaccountlink", "updated_at")
    op.drop_column("accountpermissionaccountlink", "created_at")
    op.drop_column("accountpermission", "updated_at")
    op.drop_column("accountpermission", "created_at")
    op.drop_column("accountmodel", "updated_at")
    op.drop_column("accountmodel", "created_at")
    # ### end Alembic commands ###
