import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import QDRANT_URL, QDRANT_API_KEY
from retrieval_validation.models import RetrievedChunk

logger = logging.getLogger(__name__)

class QdrantSearchClient:
    """
    Handles similarity search operations against Qdrant Cloud
    """

    def __init__(self):
        """
        Initialize the Qdrant client
        """
        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=10
        )

    def search_similar_chunks(
        self,
        query_embedding: List[float],
        collection_name: str = "book_embedding",
        top_k: int = 5,
        metadata_filters: Optional[Dict[str, str]] = None
    ) -> List[RetrievedChunk]:
        """
        Perform similarity search against Qdrant collection

        Args:
            query_embedding: The embedding vector to search for
            collection_name: Name of the Qdrant collection to search
            top_k: Number of top results to return
            metadata_filters: Optional metadata filters to apply

        Returns:
            List of RetrievedChunk objects containing the search results
        """
        try:
            # Build filter conditions if metadata filters are provided
            search_filter = None
            if metadata_filters:
                filter_conditions = []
                for field, value in metadata_filters.items():
                    # Add condition for exact match on metadata field
                    filter_conditions.append(
                        models.FieldCondition(
                            key=f"chunk_metadata.{field}",
                            match=models.MatchValue(value=value)
                        )
                    )

                if filter_conditions:
                    search_filter = models.Filter(
                        must=filter_conditions
                    )

            # Perform the search
            search_results = self.client.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter,
                with_payload=True
            )

            # Convert results to RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                payload = result.payload

                chunk = RetrievedChunk(
                    content=payload.get('text_content', ''),
                    similarity_score=result.score,
                    source_url=payload.get('source_url', ''),
                    source_title=payload.get('source_title', ''),
                    metadata=payload.get('chunk_metadata', {}),
                    confidence_score=result.score  # Using similarity score as confidence
                )
                retrieved_chunks.append(chunk)

            return retrieved_chunks

        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            raise

    def search_with_filters(
        self,
        query_embedding: List[float],
        collection_name: str = "book_embedding",
        top_k: int = 5,
        url_filter: Optional[str] = None,
        module_filter: Optional[str] = None,
        section_filter: Optional[str] = None
    ) -> List[RetrievedChunk]:
        """
        Perform similarity search with specific metadata filters

        Args:
            query_embedding: The embedding vector to search for
            collection_name: Name of the Qdrant collection to search
            top_k: Number of top results to return
            url_filter: Filter by specific URL
            module_filter: Filter by module
            section_filter: Filter by section

        Returns:
            List of RetrievedChunk objects containing the search results
        """
        try:
            # Build filter conditions
            filter_conditions = []

            if url_filter:
                filter_conditions.append(
                    models.FieldCondition(
                        key="source_url",
                        match=models.MatchValue(value=url_filter)
                    )
                )

            if module_filter or section_filter:
                # Assuming module and section might be in metadata
                if module_filter:
                    filter_conditions.append(
                        models.FieldCondition(
                            key="chunk_metadata.module",
                            match=models.MatchValue(value=module_filter)
                        )
                    )

                if section_filter:
                    filter_conditions.append(
                        models.FieldCondition(
                            key="chunk_metadata.section",
                            match=models.MatchValue(value=section_filter)
                        )
                    )

            search_filter = None
            if filter_conditions:
                search_filter = models.Filter(
                    must=filter_conditions
                )

            # Perform the search
            search_results = self.client.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter,
                with_payload=True
            )

            # Convert results to RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                payload = result.payload

                chunk = RetrievedChunk(
                    content=payload.get('text_content', ''),
                    similarity_score=result.score,
                    source_url=payload.get('source_url', ''),
                    source_title=payload.get('source_title', ''),
                    metadata=payload.get('chunk_metadata', {}),
                    confidence_score=result.score  # Using similarity score as confidence
                )
                retrieved_chunks.append(chunk)

            return retrieved_chunks

        except Exception as e:
            logger.error(f"Error performing filtered similarity search: {e}")
            raise

# Global instance for use throughout the application
qdrant_client = QdrantSearchClient()