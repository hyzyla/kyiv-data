"""Add location table

Revision ID: 8bc6efdf0f2c
Revises: 123318fed55c
Create Date: 2020-12-19 09:30:12.399643

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8bc6efdf0f2c'
down_revision = '123318fed55c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ticket_location',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('lat', sa.Float(), nullable=False),
        sa.Column('lng', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.drop_column('tickets', 'location_lng')
    op.drop_column('tickets', 'location_lat')


def downgrade():
    op.add_column(
        'tickets',
        sa.Column('location_lat', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    )
    op.add_column(
        'tickets',
        sa.Column('location_lng', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    )
    op.drop_table('ticket_location')
