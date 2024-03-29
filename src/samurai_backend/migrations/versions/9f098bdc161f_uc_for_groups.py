"""UC for groups

Revision ID: 9f098bdc161f
Revises: 7d1b0a6a4a73
Create Date: 2024-03-26 17:28:08.512987

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "9f098bdc161f"
down_revision = "7d1b0a6a4a73"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("group_name_faculty_id_uc", "groupmodel", ["name", "faculty_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("group_name_faculty_id_uc", "groupmodel", type_="unique")
    # ### end Alembic commands ###
