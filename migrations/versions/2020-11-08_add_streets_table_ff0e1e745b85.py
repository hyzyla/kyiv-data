"""Add streets table

Revision ID: ff0e1e745b85
Revises: 10afa4dcc25a
Create Date: 2020-11-08 09:43:08.524058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff0e1e745b85'
down_revision = '10afa4dcc25a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'streets',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('district', sa.Text(), nullable=False),
        sa.Column('document', sa.Text(), nullable=False),
        sa.Column('document_date', sa.Text(), nullable=False),
        sa.Column('document_title', sa.Text(), nullable=False),
        sa.Column('document_number', sa.Text(), nullable=False),
        sa.Column('old_category', sa.Text(), nullable=True),
        sa.Column('old_name', sa.Text(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('streets')
