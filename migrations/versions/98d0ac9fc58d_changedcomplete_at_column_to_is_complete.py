"""changedcomplete_at column to is_complete

Revision ID: 98d0ac9fc58d
Revises: cc3e377b6655
Create Date: 2022-11-05 18:15:54.127344

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '98d0ac9fc58d'
down_revision = 'cc3e377b6655'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', sa.DateTime(), nullable=True))
    op.drop_column('task', 'completed_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('completed_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###
