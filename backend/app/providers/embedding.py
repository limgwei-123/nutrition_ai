from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
  @abstractmethod
  def embed_query(self, text: str) -> list[float]:
    pass

  @abstractmethod
  def embed_document(self, text: str)-> list[float]:
    pass