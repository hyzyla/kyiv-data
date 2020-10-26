"""Fix types

Revision ID: 7cb6dd1beec8
Revises: 73fe7fb722cb
Create Date: 2020-10-26 10:07:37.991626

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7cb6dd1beec8'
down_revision = '73fe7fb722cb'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE tickets
            ALTER COLUMN id TYPE bigint USING id::bigint,
            ALTER COLUMN external_id TYPE bigint USING external_id::bigint,
            ALTER COLUMN meta TYPE jsonb USING external_id::jsonb;  
        """
    )


def downgrade():
    op.execute(
        """
        ALTER TABLE tickets
            ALTER COLUMN id TYPE int USING id::int,
            ALTER COLUMN external_id TYPE int USING external_id::int,
            ALTER COLUMN meta TYPE json USING external_id::json;  
        """
    )