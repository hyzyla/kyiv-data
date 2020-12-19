"""Add source and city column for tickets

Revision ID: f4a38b9d5a8e
Revises: 60cb870a41aa
Create Date: 2020-11-21 08:51:19.855914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import Enum

from app.tickets.enums import TicketSource

revision = 'f4a38b9d5a8e'
down_revision = '60cb870a41aa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cities',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.add_column('tickets', sa.Column('city_id', sa.BigInteger(), nullable=True))
    op.add_column(
        'tickets',
        sa.Column(
            'source',
            Enum(TicketSource, native_enum=False, length=100),
            nullable=True
        ),
    )
    op.create_foreign_key(None, 'tickets', 'cities', ['city_id'], ['id'])

    op.execute(
        '''
        INSERT INTO cities (id, name) VALUES (1, 'Київ');
        UPDATE tickets SET city_id = 1;
        UPDATE tickets SET source = 'cc1551';
        ALTER TABLE tickets ALtER COLUMN city_id SET NOT NULL;
        ALTER TABLE tickets ALtER COLUMN source SET NOT NULL;
        '''
    )


def downgrade():
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_column('tickets', 'source')
    op.drop_column('tickets', 'city_id')
    op.drop_table('cities')
