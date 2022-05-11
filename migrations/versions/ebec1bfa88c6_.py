"""empty message

Revision ID: ebec1bfa88c6
Revises: 1a0d4204e52d
Create Date: 2022-05-10 18:38:32.566078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebec1bfa88c6'
down_revision = '1a0d4204e52d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.add_column('task', sa.Column('is_complete', sa.Boolean(), nullable=True))
    op.drop_column('task', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('task_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('task', 'is_complete')
    op.drop_column('task', 'id')
    # ### end Alembic commands ###