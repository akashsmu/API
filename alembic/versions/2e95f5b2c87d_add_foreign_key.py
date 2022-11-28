"""add foreign key

Revision ID: 2e95f5b2c87d
Revises: db03498cd3ca
Create Date: 2022-11-27 18:48:36.812089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e95f5b2c87d'
down_revision = 'db03498cd3ca'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('posts',sa.Column('user_id',sa.Integer(),nullable = False))
    op.create_foreign_key('posts_users_fk',source_table='posts', referent_table='users',local_cols = ['user_id'], remote_cols=['id'],ondelete='Cascade')

    pass


def downgrade() :
    op.drop_constraint('post_users_fk',table_name= 'posts')
    op.drop_column('posts','user_id')
    pass
