"""add foreign key to posts table

Revision ID: 564578e43acb
Revises: bb4498199c65
Create Date: 2023-02-01 10:32:23.433452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '564578e43acb'
down_revision = 'bb4498199c65'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    
    pass
