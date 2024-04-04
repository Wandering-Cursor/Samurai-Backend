"""Comments models

Revision ID: 122480cc7adf
Revises: af1da0d02da9
Create Date: 2024-04-04 19:10:05.012642

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "122480cc7adf"
down_revision = "af1da0d02da9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "filemodel",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("file_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("file_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("file_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("file_path", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("file_id"),
    )
    op.create_table(
        "commentmodel",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("file_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("text", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("comment_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("task_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("sender_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sender_id"],
            ["accountmodel.account_id"],
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["usertaskmodel.task_id"],
        ),
        sa.PrimaryKeyConstraint("comment_id"),
    )
    op.create_index(
        op.f("ix_commentmodel_comment_id"), "commentmodel", ["comment_id"], unique=False
    )
    op.create_index(op.f("ix_commentmodel_sender_id"), "commentmodel", ["sender_id"], unique=False)
    op.create_index(op.f("ix_commentmodel_task_id"), "commentmodel", ["task_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_commentmodel_task_id"), table_name="commentmodel")
    op.drop_index(op.f("ix_commentmodel_sender_id"), table_name="commentmodel")
    op.drop_index(op.f("ix_commentmodel_comment_id"), table_name="commentmodel")
    op.drop_table("commentmodel")
    op.drop_table("filemodel")
    # ### end Alembic commands ###
