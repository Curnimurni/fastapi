"""create posts table

Revision ID: b9c2dd8bfb74
Revises: 
Create Date: 2023-01-31 13:03:42.897887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9c2dd8bfb74'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key=True),sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
