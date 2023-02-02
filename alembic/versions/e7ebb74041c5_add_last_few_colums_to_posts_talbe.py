"""add last few colums to posts talbe

Revision ID: e7ebb74041c5
Revises: 564578e43acb
Create Date: 2023-02-01 11:11:53.413613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7ebb74041c5'
down_revision = '564578e43acb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_deafault='True'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),)

    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
