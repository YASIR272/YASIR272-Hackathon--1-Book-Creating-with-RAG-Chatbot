import time
import logging
from typing import List, Dict, Any, Optional
from config.logging import logger
from services.qdrant_service import qdrant_service
from models.agent_models import RetrievedChunk


class RetrievalService:
    """
    Service for handling retrieval operations from Qdrant
    """

    def __init__(self):
        self.logger = logger

    def retrieve_context(
        self,
        query_embedding: List[float],
        collection_name: str = "book_embedding",
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[RetrievedChunk]:
        """
        Retrieve context from Qdrant based on the query embedding

        Args:
            query_embedding: The embedding vector to search for
            collection_name: Name of the Qdrant collection to search
            top_k: Number of top results to return
            filters: Optional filters to apply to the search

        Returns:
            List of RetrievedChunk objects
        """
        start_time = time.time()
        self.logger.info(f"Starting retrieval from collection '{collection_name}' with top_k={top_k}")

        try:
            # Search in Qdrant
            search_results = qdrant_service.search_similar(
                collection_name=collection_name,
                query_vector=query_embedding,
                top_k=top_k,
                filters=filters
            )

            # Convert results to RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                chunk = RetrievedChunk(
                    id=result['id'],
                    content=result['content'],
                    similarity_score=result['score'],
                    source_url=result['source_url'],
                    source_title=result['source_title'],
                    metadata=result['metadata']
                )
                retrieved_chunks.append(chunk)

            retrieval_time = time.time() - start_time
            self.logger.info(f"Retrieved {len(retrieved_chunks)} chunks in {retrieval_time:.2f}s")

            return retrieved_chunks

        except Exception as e:
            retrieval_time = time.time() - start_time
            self.logger.error(f"Error during retrieval after {retrieval_time:.2f}s: {e}")
            raise

    def retrieve_context_with_scope(
        self,
        query_embedding: List[float],
        scope: str = "full_book",
        scope_filters: Optional[Dict[str, Any]] = None,
        collection_name: str = "book_embedding",
        top_k: int = 5
    ) -> List[RetrievedChunk]:
        """
        Retrieve context from Qdrant with scope-based filtering

        Args:
            query_embedding: The embedding vector to search for
            scope: The scope of the query ("full_book" or "selected_text")
            scope_filters: Filters to apply based on scope (for "selected_text" mode)
            collection_name: Name of the Qdrant collection to search
            top_k: Number of top results to return

        Returns:
            List of RetrievedChunk objects
        """
        start_time = time.time()
        self.logger.info(f"Starting scoped retrieval (scope: {scope}) from collection '{collection_name}' with top_k={top_k}")

        try:
            # Prepare filters based on scope
            filters = {}
            if scope == "selected_text" and scope_filters:
                # Apply the scope filters for selected text mode
                filters.update(scope_filters)
                self.logger.info(f"Applying scope filters: {scope_filters}")
            elif scope == "full_book":
                self.logger.info("Using full book scope - no additional filters applied")
            else:
                self.logger.warning(f"Unknown scope '{scope}', defaulting to full book")

            # Search in Qdrant with the prepared filters
            search_results = qdrant_service.search_similar(
                collection_name=collection_name,
                query_vector=query_embedding,
                top_k=top_k,
                filters=filters if filters else None
            )

            # Convert results to RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                chunk = RetrievedChunk(
                    id=result['id'],
                    content=result['content'],
                    similarity_score=result['score'],
                    source_url=result['source_url'],
                    source_title=result['source_title'],
                    metadata=result['metadata']
                )
                retrieved_chunks.append(chunk)

            retrieval_time = time.time() - start_time
            self.logger.info(f"Scoped retrieval completed: {len(retrieved_chunks)} chunks in {retrieval_time:.2f}s")

            return retrieved_chunks

        except Exception as e:
            retrieval_time = time.time() - start_time
            self.logger.error(f"Error during scoped retrieval after {retrieval_time:.2f}s: {e}")
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
            return qdrant_service.get_collection_info(collection_name)
        except Exception as e:
            self.logger.error(f"Error getting collection info: {e}")
            raise


# Global instance
retrieval_service = RetrievalService()