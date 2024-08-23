"""add content column

Revision ID: 36037f23cda5
Revises: 48f7ce491f35
Create Date: 2024-08-20 19:33:06.366255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36037f23cda5'
down_revision: Union[str, None] = '48f7ce491f35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
