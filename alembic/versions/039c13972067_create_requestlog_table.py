"""Create RequestLog table

Revision ID: 039c13972067
Revises: 374fc3317ec8
Create Date: 2023-07-09 17:59:10.919412

"""
from alembic import op
import sqlalchemy as sa
import fastapi_utils

# revision identifiers, used by Alembic.
revision = '039c13972067'
down_revision = '374fc3317ec8'
branch_labels = None
depends_on = None


def upgrade() -> None:
   op.create_table(
        'request_logs',
        sa.Column('id', fastapi_utils.guid_type.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('method', sa.String(length=255), nullable=True),
        sa.Column('url', sa.String(length=255), nullable=True),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('request_logs')