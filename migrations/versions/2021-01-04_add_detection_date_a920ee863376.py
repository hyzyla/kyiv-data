"""Add detection date

Revision ID: a920ee863376
Revises: ff33762efa16
Create Date: 2021-01-04 18:43:20.701001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a920ee863376'
down_revision = 'ff33762efa16'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tickets', sa.Column('detection_date', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('tickets', 'detection_date')
