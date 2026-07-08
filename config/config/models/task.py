from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Task(BaseModel):
    title: str
    due_date: Optional[str] = None
    completed: bool = False
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None
    
    def mark_completed(self):
        self.completed = True
        self.completed_at = datetime.now()
    
    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }