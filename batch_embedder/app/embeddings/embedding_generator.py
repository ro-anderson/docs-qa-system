import openai
from core.settings import get_settings
from core.logger import logger

class EmbeddingGenerator:
    def __init__(self):
        settings = get_settings()
        self.model = settings.EMBEDDING_MODEL
        openai.api_key = settings.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        logger.info(f"Initialized EmbeddingGenerator with model: {self.model}")

    def generate_embedding(self, text: str) -> list:
        """Generate embedding for given text using OpenAI API"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding for text of length: {len(text)}")
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise e