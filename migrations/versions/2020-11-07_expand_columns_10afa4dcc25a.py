"""Expand columns

Revision ID: 10afa4dcc25a
Revises: 7cb6dd1beec8
Create Date: 2020-11-07 08:47:59.378573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '10afa4dcc25a'
down_revision = '7cb6dd1beec8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tickets', sa.Column('address', sa.Text(), nullable=True))
    op.add_column('tickets', sa.Column('approx_done_date', sa.Date(), nullable=True))
    op.add_column('tickets', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('tickets', sa.Column('status', sa.Text(), nullable=True))
    op.add_column('tickets', sa.Column('subject_id', sa.Text(), nullable=True))
    op.add_column('tickets', sa.Column('title', sa.Text(), nullable=True))
    op.add_column('tickets', sa.Column('work_taken_by', sa.Text(), nullable=True))

    op.execute(
        """
            UPDATE tickets
            SET title = meta ->> 'title',
                status = meta ->> 'status',
                address = meta ->> 'address',
                work_taken_by = meta ->> 'work_taken_by',
                approx_done_date = (meta ->> 'approx_done_date')::date,
                created_at = (meta ->> 'created_at')::timestamp with time zone,
                subject_id = meta -> 'subject' ->> 'id'
        """
    )

    op.execute(
        """
        ALTER TABLE tickets ALTER COLUMN approx_done_date SET NOT NULL;
        ALTER TABLE tickets ALTER COLUMN created_at SET NOT NULL;
        ALTER TABLE tickets ALTER COLUMN status SET NOT NULL;
        ALTER TABLE tickets ALTER COLUMN subject_id SET NOT NULL;
        ALTER TABLE tickets ALTER COLUMN title SET NOT NULL;
        ALTER TABLE tickets ALTER COLUMN work_taken_by SET NOT NULL;
        """
    )

    op.alter_column(
        'tickets',
        'meta',
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        nullable=False
    )


def downgrade():
    op.alter_column(
        'tickets',
        'meta',
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        nullable=True
    )
    op.drop_column('tickets', 'work_taken_by')
    op.drop_column('tickets', 'title')
    op.drop_column('tickets', 'subject_id')
    op.drop_column('tickets', 'status')
    op.drop_column('tickets', 'created_at')
    op.drop_column('tickets', 'approx_done_date')
    op.drop_column('tickets', 'address')
