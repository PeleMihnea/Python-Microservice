from sqlalchemy import Column, Integer, String, DateTime, JSON
from math_microservice.db.base import Base
import datetime

class RequestLog(Base):
    __tablename__ = "request_logs"
    id        = Column(Integer, primary_key=True, index=True)
    path      = Column(String, index=True)
    payload   = Column(JSON)
    response  = Column(JSON)
    ts        = Column(DateTime, default=datetime.datetime.utcnow)
