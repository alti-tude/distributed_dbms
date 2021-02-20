from abc import ABC
import abc

class BasePrimitive(abc.ABC):
    @abc.abstractmethod
    def to_dict(self):
        return {}
    
    def __repr__(self) -> str:
        return str(self.to_dict())