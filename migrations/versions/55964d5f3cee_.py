"""empty message

Revision ID: 55964d5f3cee
Revises: 4c09713bb1c7
Create Date: 2019-11-17 19:41:45.863348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55964d5f3cee'
down_revision = '4c09713bb1c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('shows_venue_id_fkey', 'shows', type_='foreignkey')
    op.create_foreign_key(None, 'shows', 'venues', ['venue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.create_foreign_key('shows_venue_id_fkey', 'shows', 'shows', ['venue_id'], ['id'])
    # ### end Alembic commands ###
