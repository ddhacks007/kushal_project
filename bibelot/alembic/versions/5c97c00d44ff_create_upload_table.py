"""create upload table

Revision ID: 5c97c00d44ff
Revises: 
Create Date: 2019-03-23 18:42:15.800831

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = '5c97c00d44ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('create table uploads (id serial primary key, shop_name text, file_date date, upload_time  TIMESTAMP DEFAULT CURRENT_TIMESTAMP, type text)')

def downgrade():
    op.execute('drop table uploads')