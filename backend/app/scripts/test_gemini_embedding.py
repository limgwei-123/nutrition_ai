from app.core.config import settings

from app.providers.gemini_embedding import VertexEmbeddingProvider

def main():
  provider = VertexEmbeddingProvider(
    api_key=settings.gemini_api_key,
    model=settings.gemini_embedding_model,
  )

  embedding = provider.embed_query("egg")

  print("Embedding length:", len(embedding))
  print("First 5 values:", embedding[:5])

if __name__ == "__main__":
    main()