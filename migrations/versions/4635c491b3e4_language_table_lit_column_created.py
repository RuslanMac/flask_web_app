"""language table lit column created

Revision ID: 4635c491b3e4
Revises: e69940135246
Create Date: 2020-08-13 23:09:04.689305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4635c491b3e4'
down_revision = 'e69940135246'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('language', sa.Column('lit', sa.String(length=4), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('language', 'lit')
    # ### end Alembic commands ###