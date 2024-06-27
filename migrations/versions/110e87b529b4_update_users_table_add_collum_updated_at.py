"""Update users table (add collum updated_at)

Revision ID: 110e87b529b4
Revises: 2dd52ae7df0b
Create Date: 2024-06-27 10:55:46.990499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '110e87b529b4'
down_revision: Union[str, None] = '2dd52ae7df0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'updated_at')
    # ### end Alembic commands ###