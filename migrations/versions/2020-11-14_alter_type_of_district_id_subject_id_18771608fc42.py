"""Alter type of district_id, subject_id

Revision ID: 18771608fc42
Revises: 95ea288c728a
Create Date: 2020-11-14 09:58:38.709804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18771608fc42'
down_revision = '95ea288c728a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE tickets
            ALTER COLUMN subject_id TYPE bigint USING id::bigint,
            ALTER COLUMN district_id TYPE bigint USING external_id::bigint;
        """
    )


def downgrade():
    op.execute(
        """
        ALTER TABLE tickets
            ALTER COLUMN subject_id TYPE text USING id::text,
            ALTER COLUMN district_id TYPE text USING external_id::text;
        """
    )
