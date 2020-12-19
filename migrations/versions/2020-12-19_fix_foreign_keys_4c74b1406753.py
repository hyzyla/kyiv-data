"""Fix foreign keys

Revision ID: 4c74b1406753
Revises: 8bc6efdf0f2c
Create Date: 2020-12-19 09:36:48.547462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c74b1406753'
down_revision = '8bc6efdf0f2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket_location', sa.Column('ticket_id', sa.BigInteger(), nullable=True))
    op.create_unique_constraint(None, 'ticket_location', ['ticket_id'])
    op.create_foreign_key(None, 'ticket_location', 'tickets', ['ticket_id'], ['id'])
    op.add_column('tickets_photos', sa.Column('ticket_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'tickets_photos', 'tickets', ['ticket_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tickets_photos', type_='foreignkey')
    op.drop_column('tickets_photos', 'ticket_id')
    op.drop_constraint(None, 'ticket_location', type_='foreignkey')
    op.drop_constraint(None, 'ticket_location', type_='unique')
    op.drop_column('ticket_location', 'ticket_id')
    # ### end Alembic commands ###
