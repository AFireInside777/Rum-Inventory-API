"""empty message

Revision ID: 91dddba13164
Revises: 
Create Date: 2024-03-13 13:47:21.820063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91dddba13164'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rum',
    sa.Column('rum_id', sa.String(length=150), nullable=False),
    sa.Column('rum_company', sa.String(length=150), nullable=False),
    sa.Column('rum_name', sa.String(length=150), nullable=False),
    sa.Column('rum_age', sa.String(length=150), nullable=True),
    sa.Column('rum_stock_qty', sa.Integer(), nullable=True),
    sa.Column('rum_price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('rum_id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('g_auth_verify', sa.Boolean(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('rum')
    # ### end Alembic commands ###
