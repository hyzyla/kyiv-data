"""Add photo content type

Revision ID: 58619489f248
Revises: 19ae468b7062
Create Date: 2020-12-19 13:33:19.435291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58619489f248'
down_revision = '19ae468b7062'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets_photos', sa.Column('content_type', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tickets_photos', 'content_type')
    # ### end Alembic commands ###
