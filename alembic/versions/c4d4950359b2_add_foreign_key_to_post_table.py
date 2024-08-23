"""Add foreign key to post table

Revision ID: c4d4950359b2
Revises: 2250724fda5a
Create Date: 2024-08-20 19:46:15.810082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4d4950359b2'
down_revision: Union[str, None] = '2250724fda5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', 
                                     sa.Integer(), 
                                     nullable=False))
    op.create_foreign_key('post_user_fk', 
                          source_table='posts', 
                          referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE') 
                                     
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
