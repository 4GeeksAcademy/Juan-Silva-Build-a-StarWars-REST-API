"""empty message

Revision ID: 06639248e661
Revises: f4bed43adea0
Create Date: 2023-05-10 18:59:38.875432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06639248e661'
down_revision = 'f4bed43adea0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('hair_color', sa.String(length=80), nullable=True),
    sa.Column('gender', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('people')
    # ### end Alembic commands ###