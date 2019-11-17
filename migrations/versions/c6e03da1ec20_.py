"""empty message

Revision ID: c6e03da1ec20
Revises: 8b81ff992278
Create Date: 2019-11-17 12:06:56.765693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6e03da1ec20'
down_revision = '8b81ff992278'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('address', sa.String(length=120), nullable=True))
    op.add_column('artists', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('artists', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.add_column('artists', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('shows', sa.Column('artist_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'shows', 'shows', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_column('shows', 'artist_id')
    op.drop_column('artists', 'website')
    op.drop_column('artists', 'date_modified')
    op.drop_column('artists', 'date_created')
    op.drop_column('artists', 'address')
    # ### end Alembic commands ###