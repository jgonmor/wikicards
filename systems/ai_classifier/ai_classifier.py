from abc import ABC, abstractmethod

class AIClassifier(ABC):
    @abstractmethod
    def classify(self, title: str, description: str, categories: list[str]) -> str:
        pass
    
    @abstractmethod
    def classify_batch(self, articles: list[dict], categories: list[str]) -> list[str]:
        pass