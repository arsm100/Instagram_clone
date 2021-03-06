"""added a column to track whether a user is private and indexed username and email

Revision ID: 482cfd2de46f
Revises: 06fdac92a3c4
Create Date: 2018-11-27 17:42:20.941609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '482cfd2de46f'
down_revision = '06fdac92a3c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_private', sa.Boolean(),
                                     server_default='False', nullable=False))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'),
                    'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'is_private')
    # ### end Alembic commands ###
