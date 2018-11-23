"""added profile picture URL column

Revision ID: 86620fb9326d
Revises: 7727667f93fb
Create Date: 2018-11-23 17:24:57.437262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86620fb9326d'
down_revision = '7727667f93fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_picture_URL', sa.Text(), server_default='https://s3.amazonaws.com/ahmed-clone-instagram/generic_profile_pic.png', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_picture_URL')
    # ### end Alembic commands ###
