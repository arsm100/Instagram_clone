"""created many-to-many relationship between users

Revision ID: 8db4e7e07869
Revises: 466e6376acbc
Create Date: 2018-11-30 02:01:00.420408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8db4e7e07869'
down_revision = '466e6376acbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('follower_id', sa.Integer(), nullable=False),
                    sa.Column('followed_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_users')
    # ### end Alembic commands ###
