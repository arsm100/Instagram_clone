"""added image captions column

Revision ID: 06fdac92a3c4
Revises: 35fb7cad0017
Create Date: 2018-11-26 11:44:47.398646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06fdac92a3c4'
down_revision = '35fb7cad0017'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('image_caption', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images', 'image_caption')
    # ### end Alembic commands ###
