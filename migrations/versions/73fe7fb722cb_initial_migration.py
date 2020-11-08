"""Initial migration.

Revision ID: 73fe7fb722cb
Revises: 
Create Date: 2020-10-20 08:52:47.129473

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '73fe7fb722cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('number', sa.Text(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('external_id', sa.Text(), nullable=False),
        sa.Column('meta', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_tickets_external_id'), 'tickets', ['external_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_tickets_external_id'), table_name='tickets')
    op.drop_table('tickets')
