"""adding campaign user relationship

Revision ID: 2ebf439f9bf5
Revises: af383853ef17
Create Date: 2020-10-01 11:22:21.620427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ebf439f9bf5'
down_revision = 'af383853ef17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaigns', sa.Column('created_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('campaigns', 'created_date')
    # ### end Alembic commands ###
