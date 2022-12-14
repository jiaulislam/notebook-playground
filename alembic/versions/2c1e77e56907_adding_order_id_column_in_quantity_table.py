"""adding order_id column in Quantity Table

Revision ID: 2c1e77e56907
Revises: 2e0bf557e78b
Create Date: 2022-12-18 22:46:44.192186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c1e77e56907'
down_revision = '2e0bf557e78b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_order_quantities', sa.Column('order_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'product_order_quantities', 'orderes', ['order_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_order_quantities', type_='foreignkey')
    op.drop_column('product_order_quantities', 'order_id')
    # ### end Alembic commands ###
