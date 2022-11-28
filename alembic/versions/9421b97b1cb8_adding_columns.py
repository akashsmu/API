"""adding columns

Revision ID: 9421b97b1cb8
Revises: 312ec6bed5f8
Create Date: 2022-11-27 18:36:34.374793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9421b97b1cb8'
down_revision = '312ec6bed5f8'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('posts',sa.Column('content',sa.String(), nullable= False))
    pass


def downgrade() :
    op.drop_column('posts','content')
    pass
