from datetime import datetime
from database import Base, session_scope
import sqlalchemy as sa
from enum import Enum


class BaseModel(Base):
    """Base data model for all objects"""
    __abstract__ = True


class Upload(BaseModel):
    __tablename__ = 'uploads'
    shop_name = sa.Column('shop_name', sa.Text, primary_key=True)
    file_date = sa.Column('file_date', sa.Date)
    upload_time = sa.Column('upload_time', sa.DateTime, default=datetime.now())
    type_of_file = sa.Column('type', sa.Text)

    @staticmethod
    def create(shop_name, file_date, type_of_file):
        with session_scope() as session:
            upload = Upload()
            upload.file_date = file_date
            upload.shop_name = shop_name
            upload.type_of_file = type_of_file
            session.add(upload)