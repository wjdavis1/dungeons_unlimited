"""change class declaration

Revision ID: 15cde4fac7fd
Revises: 6ce70a8ac4ff
Create Date: 2020-10-19 00:00:47.196900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15cde4fac7fd'
down_revision = '6ce70a8ac4ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character_name', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_character_character_name'), 'character', ['character_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_character_character_name'), table_name='character')
    op.drop_table('character')
    # ### end Alembic commands ###
