"""empty message

Revision ID: 4c09713bb1c7
Revises: c6e03da1ec20
Create Date: 2019-11-17 13:22:23.546988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c09713bb1c7'
down_revision = 'c6e03da1ec20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.drop_column('artists', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('artists', 'seeking_venue')
    # ### end Alembic commands ###
