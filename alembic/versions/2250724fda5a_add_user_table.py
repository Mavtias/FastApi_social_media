"""add user table

Revision ID: 2250724fda5a
Revises: 36037f23cda5
Create Date: 2024-08-20 19:38:30.130512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2250724fda5a'
down_revision: Union[str, None] = '36037f23cda5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                     sa.Column('email', sa.String(), nullable=False, unique=True), 
                     sa.Column('password', sa.String(), nullable=False), 
                     sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                               server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
