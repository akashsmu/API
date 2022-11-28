"""add user table

Revision ID: db03498cd3ca
Revises: 9421b97b1cb8
Create Date: 2022-11-27 18:40:45.541348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db03498cd3ca'
down_revision = '9421b97b1cb8'
branch_labels = None
depends_on = None


def upgrade() :
    op.create_table('users',
    sa.Column('id',sa.Integer(), nullable = False),
    sa.Column('email',sa.String(),nullable = False),
    sa.Column('password',sa.String(),nullable = False),
    sa.Column('create_at',sa.TIMESTAMP(timezone=True),
    server_default = sa.text('now()'),nullable = False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))
    pass


def downgrade() :
    op.drop_table('users')
    pass
