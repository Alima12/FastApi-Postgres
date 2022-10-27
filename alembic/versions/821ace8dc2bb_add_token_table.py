"""add token table

Revision ID: 821ace8dc2bb
Revises: 9c21df4c40d6
Create Date: 2022-10-26 17:58:48.582057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '821ace8dc2bb'
down_revision = '9c21df4c40d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokens',
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('is_expired', sa.Boolean(), server_default='False', nullable=True),
    sa.PrimaryKeyConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens')
    # ### end Alembic commands ###