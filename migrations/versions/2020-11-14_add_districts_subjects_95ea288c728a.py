"""Add districts, subjects

Revision ID: 95ea288c728a
Revises: bd0d7ec077b4
Create Date: 2020-11-14 09:35:40.459550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from app.tickets.constants import SUBJECTS, DISTRICTS
from app.tickets.models import District, Subject

revision = '95ea288c728a'
down_revision = 'bd0d7ec077b4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'districts',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'subjects',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_tickets_district_id'), 'tickets', ['district_id'], unique=False)
    op.create_index(op.f('ix_tickets_subject_id'), 'tickets', ['subject_id'], unique=False)

    op.bulk_insert(Subject.__table__, SUBJECTS)
    op.bulk_insert(District.__table__, DISTRICTS)


def downgrade():
    op.drop_index(op.f('ix_tickets_subject_id'), table_name='tickets')
    op.drop_index(op.f('ix_tickets_district_id'), table_name='tickets')
    op.drop_table('subjects')
    op.drop_table('districts')
