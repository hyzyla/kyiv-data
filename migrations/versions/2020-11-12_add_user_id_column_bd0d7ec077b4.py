"""Add user_id column

Revision ID: bd0d7ec077b4
Revises: cdbfb33c05e0
Create Date: 2020-11-12 17:01:35.753226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd0d7ec077b4'
down_revision = 'cdbfb33c05e0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tickets', sa.Column('user_id', sa.Text(), nullable=True))
    op.execute(
        """
            UPDATE tickets
            SET user_id = meta ->> 'user_id';
        """
    )

    op.execute(
        """
        ALTER TABLE tickets ALTER COLUMN user_id SET NOT NULL;
        """
    )


def downgrade():
    op.drop_column('tickets', 'user_id')
