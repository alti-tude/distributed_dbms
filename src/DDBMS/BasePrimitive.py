from abc import ABC
import abc

class BasePrimitive(abc.ABC):
    @abc.abstractmethod
    def to_dict(self):
        return {}
    
    def compact_display(self):
        return ""
    
    def __str__(self) -> str:
        return repr(self)
        
    def __repr__(self) -> str:
        return str(self.to_dict())

    def __hash__(self) -> int:
        return hash(repr(self))
    
    def __eq__(self, o: object) -> bool:
        return repr(self) == repr(o)
