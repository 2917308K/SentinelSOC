from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.models.event import Event


class DetectionRule(ABC):
    rule_id: str
    name: str
    description: str

    @abstractmethod
    def evaluate(
        self,
        db: Session,
        event: Event,
    ) -> dict | None:
        
        raise NotImplementedError