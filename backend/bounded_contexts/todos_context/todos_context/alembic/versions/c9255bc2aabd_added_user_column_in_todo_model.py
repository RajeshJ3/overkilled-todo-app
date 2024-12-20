"""added user column in todo model

Revision ID: c9255bc2aabd
Revises: c5fcf8bf8355
Create Date: 2024-12-20 06:42:32.320988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9255bc2aabd'
down_revision: Union[str, None] = 'c5fcf8bf8355'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('user', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'todos', 'users', ['user'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'user')
    # ### end Alembic commands ###
