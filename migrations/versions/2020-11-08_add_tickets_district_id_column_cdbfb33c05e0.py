"""Add tickets.district_id column

Revision ID: cdbfb33c05e0
Revises: 9d95b1c4dfed
Create Date: 2020-11-08 16:12:09.393386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdbfb33c05e0'
down_revision = '9d95b1c4dfed'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('TRUNCATE tickets;')
    op.add_column('tickets', sa.Column('district_id', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('tickets', 'district_id')
