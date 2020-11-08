"""Fix streets columns

Revision ID: 9d95b1c4dfed
Revises: ff0e1e745b85
Create Date: 2020-11-08 10:35:20.577914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d95b1c4dfed'
down_revision = 'ff0e1e745b85'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('streets', 'comment', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('streets', 'document', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('streets', 'document_date', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('streets', 'document_number', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('streets', 'document_title', existing_type=sa.TEXT(), nullable=True)


def downgrade():
    op.alter_column('streets', 'document_title', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('streets', 'document_number', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('streets', 'document_date', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('streets', 'document', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('streets', 'comment', existing_type=sa.TEXT(), nullable=False)
