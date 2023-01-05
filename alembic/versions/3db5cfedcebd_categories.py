"""categories

Revision ID: 3db5cfedcebd
Revises: 654f2756cbc7
Create Date: 2022-12-18 11:56:08.382002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3db5cfedcebd'
down_revision = '654f2756cbc7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, maxvalue=999999999999999999999999999, cycle=True), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_category_assoc',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, maxvalue=999999999999999999999999999, cycle=True), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('products', 'id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=False, start=1, maxvalue=999999999999999999999999999, cycle=True),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('tags', 'id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=False, start=1, maxvalue=999999999999999999999999999, cycle=True),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tags', 'id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=False, on_null=False, start=1, increment=1, minvalue=1, maxvalue=9999999999999999999999999999, cycle=False, cache=20, order=False),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('products', 'id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=False, on_null=False, start=1, increment=1, minvalue=1, maxvalue=9999999999999999999999999999, cycle=False, cache=20, order=False),
               existing_nullable=False,
               autoincrement=True)
    op.drop_table('product_category_assoc')
    op.drop_table('categories')
    # ### end Alembic commands ###