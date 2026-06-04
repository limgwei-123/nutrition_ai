from google import genai
from google.genai import types

class GeminiEmbeddingProvider:

  def __init__(
    self,
    api_key: str,
    model: str = "gemini-embedding-001"
    ):
      self.client = genai.Client(api_key=api_key)
      self.model = model

  def embed_query(self, text: str) -> list[float]:
    return self._embed(text, task_type="RETRIEVAL_QUERY")

  def embed_document(self, text: str) -> list[float]:
    return self._embed(text, task_type="RETRIEVAL_DOCUMENT")

  def _embed(self, text: str, task_type: str) ->list[float]:
    response = self.client.models.embed_content(
      model = self.model,
      contents=text,
      config=types.EmbedContentConfig(
        task_type=task_type
      )
    )

    embeddings = response.embeddings[0].values
    return list(embeddings)