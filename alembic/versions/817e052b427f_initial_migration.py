"""initial migration
Revision ID: 817e052b427f
Revises: bc8ead7d6cbb
Create Date: 2024-05-05 03:53:32.072778
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '817e052b427f'
down_revision: Union[str, None] = 'bc8ead7d6cbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('events_created_by_fkey', 'events', type_='foreignkey')
    op.drop_column('events', 'created_by')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('created_by', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('events_created_by_fkey', 'events', 'users', ['created_by'], ['id'])
    # ### end Alembic commands ###