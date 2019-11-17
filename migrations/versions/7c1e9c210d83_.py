"""empty message

Revision ID: 7c1e9c210d83
Revises: 1c6782faa000
Create Date: 2019-11-17 21:43:19.529634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c1e9c210d83'
down_revision = '1c6782faa000'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=True))
    op.add_column('venues', sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'genres')
    op.drop_column('artists', 'genres')
    # ### end Alembic commands ###
