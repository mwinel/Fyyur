"""empty message

Revision ID: 8b81ff992278
Revises: e730b35d3e2b
Create Date: 2019-11-17 11:59:29.744326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b81ff992278'
down_revision = 'e730b35d3e2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'shows', 'shows', ['venue_id'], ['id'])
    op.add_column('venues', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('venues', sa.Column('date_modified', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'date_modified')
    op.drop_column('venues', 'date_created')
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_column('shows', 'venue_id')
    # ### end Alembic commands ###
