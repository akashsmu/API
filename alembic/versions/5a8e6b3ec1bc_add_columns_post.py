"""add columns post

Revision ID: 5a8e6b3ec1bc
Revises: 2e95f5b2c87d
Create Date: 2022-11-27 18:53:59.197277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a8e6b3ec1bc'
down_revision = '2e95f5b2c87d'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable = False, server_default = 'TRUE'),)
    op.add_column('posts',sa.Column('create_at', sa.TIMESTAMP(timezone= True), nullable = False , server_default = sa.text('NOW()')),)
    pass


def downgrade() :
    op.drop_column('posts','published')
    op.drop_column('posts',"create_at")
    pass
