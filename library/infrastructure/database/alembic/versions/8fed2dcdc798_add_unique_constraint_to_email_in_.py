"""Add unique constraint to email in members table

Revision ID: 8fed2dcdc798
Revises: 
Create Date: 2025-01-20 11:40:00.111194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fed2dcdc798'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'members',
        sa.Column('member_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'books',
        sa.Column('book_id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('author', sa.String, nullable=False),
        sa.Column('is_borrowed', sa.Boolean, default=False, nullable=False),
        sa.Column('borrowed_date', sa.DateTime, default=None, nullable=True),
        sa.Column('borrowed_by', sa.Integer, sa.ForeignKey('members.member_id'), nullable=True),
    )
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    op.drop_table('members')
    # ### end Alembic commands ###
