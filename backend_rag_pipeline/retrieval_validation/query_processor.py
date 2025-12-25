import logging
from typing import List, Dict, Any
from config import COHERE_API_KEY
import cohere

logger = logging.getLogger(__name__)

class QueryProcessor:
    """
    Handles query processing including embedding conversion and validation
    """

    def __init__(self):
        """
        Initialize the query processor with Cohere client
        """
        self.co = cohere.Client(COHERE_API_KEY)

    def convert_query_to_embedding(self, query_text: str) -> List[float]:
        """
        Convert a query text to embedding vector using Cohere API

        Args:
            query_text: The text query to convert to embedding

        Returns:
            List[float]: The embedding vector

        Raises:
            Exception: If there's an error with the Cohere API call
        """
        try:
            response = self.co.embed(
                texts=[query_text],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Error generating embedding for query: {e}")
            raise

    def validate_query_input(self, query_text: str, top_k: int = 5, similarity_threshold: float = None) -> Dict[str, Any]:
        """
        Validate query parameters and return cleaned parameters

        Args:
            query_text: The query text to validate
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity threshold for results

        Returns:
            Dict containing validated parameters
        """
        errors = []

        # Validate query text
        if not query_text or not query_text.strip():
            errors.append("Query text cannot be empty")

        if len(query_text.strip()) < 1:
            errors.append("Query text must be at least 1 character long")

        # Validate top_k
        if top_k <= 0:
            errors.append("top_k must be greater than 0")
        if top_k > 100:  # Reasonable upper limit
            errors.append("top_k should not exceed 100")

        # Validate similarity_threshold if provided
        if similarity_threshold is not None:
            if similarity_threshold < 0.0 or similarity_threshold > 1.0:
                errors.append("similarity_threshold must be between 0.0 and 1.0")

        if errors:
            raise ValueError(f"Query validation failed: {'; '.join(errors)}")

        return {
            "query_text": query_text.strip(),
            "top_k": top_k,
            "similarity_threshold": similarity_threshold
        }

# Global instance for use throughout the application
query_processor = QueryProcessor()