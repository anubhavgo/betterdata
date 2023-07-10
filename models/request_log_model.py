from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

Base = declarative_base()

class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(
        GUID,
        primary_key=True,
        index = True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    method = Column(String)
    url = Column(String)
    status_code = Column(Integer)
    user_id = Column(String)
    created_at = Column(DateTime, default=func.now())