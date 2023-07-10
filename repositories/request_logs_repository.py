from sqlalchemy.orm import Session
from models.request_log_model import RequestLog

class RequestLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_request_log(self,log_entry):
        self.db.add(log_entry)
        self.db.commit()
        return log_entry

    def get_all_request_logs(self,offset=0, limit=1000):
        if limit > 1000: limit = 1000
        request_logs = self.db.query(RequestLog).offset(offset).limit(limit).all()
        return request_logs