"""add content column to posts table

Revision ID: b194273bfdb7
Revises: b9c2dd8bfb74
Create Date: 2023-01-31 13:42:50.446819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b194273bfdb7'
down_revision = 'b9c2dd8bfb74'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
