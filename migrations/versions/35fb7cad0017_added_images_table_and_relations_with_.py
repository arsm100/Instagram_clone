"""added images table and relations with users

Revision ID: 35fb7cad0017
Revises: 03a55452a203
Create Date: 2018-11-26 01:31:50.297746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35fb7cad0017'
down_revision = '03a55452a203'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_name', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
