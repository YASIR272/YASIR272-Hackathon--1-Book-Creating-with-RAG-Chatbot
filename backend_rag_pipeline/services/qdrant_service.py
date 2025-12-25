import logging
from typing import List, Dict, Optional, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config.settings import settings
from config.logging import logger


class QdrantService:
    """
    Service class for interacting with Qdrant vector database
    """

    def __init__(self):
        """
        Initialize the Qdrant client with configuration
        """
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=30
        )
        self.logger = logger

    def search_similar(
        self,
        collection_name: str,
        query_vector: List[float],
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the specified collection

        Args:
            collection_name: Name of the Qdrant collection to search
            query_vector: Vector to search for similarity
            top_k: Number of top results to return
            filters: Optional metadata filters to apply

        Returns:
            List of similar vectors with their payload and scores
        """
        try:
            # Build filter conditions if filters are provided
            search_filter = None
            if filters:
                filter_conditions = []

                # Add conditions for different filter types
                for field, value in filters.items():
                    if isinstance(value, list):
                        # Handle array filters (e.g., urls, modules, sections)
                        filter_conditions.append(
                            models.FieldCondition(
                                key=f"metadata.{field}",
                                match=models.MatchAny(any=value)
                            )
                        )
                    else:
                        # Handle single value filters
                        filter_conditions.append(
                            models.FieldCondition(
                                key=f"metadata.{field}",
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
                query_vector=query_vector,
                limit=top_k,
                query_filter=search_filter,
                with_payload=True,
                with_vectors=False
            )

            # Convert results to a more usable format
            results = []
            for result in search_results:
                results.append({
                    'id': result.id,
                    'score': result.score,
                    'payload': result.payload,
                    'content': result.payload.get('text_content', ''),
                    'source_url': result.payload.get('source_url', ''),
                    'source_title': result.payload.get('source_title', ''),
                    'metadata': result.payload.get('metadata', {})
                })

            self.logger.info(f"Found {len(results)} similar results in collection '{collection_name}'")
            return results

        except Exception as e:
            self.logger.error(f"Error searching in Qdrant: {e}")
            raise

    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """
        Get information about a collection

        Args:
            collection_name: Name of the collection to get info for

        Returns:
            Collection information
        """
        try:
            collection_info = self.client.get_collection(collection_name)
            return {
                'name': collection_info.name,
                'vector_size': collection_info.config.params.vectors.size,
                'distance': collection_info.config.params.vectors.distance,
                'point_count': collection_info.point_count
            }
        except Exception as e:
            self.logger.error(f"Error getting collection info: {e}")
            raise


# Global instance
qdrant_service = QdrantService()