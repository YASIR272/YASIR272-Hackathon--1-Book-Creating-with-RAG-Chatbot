import asyncio
import time
import logging
from typing import List, Dict, Any, Optional
from config.settings import settings
from config.logging import logger, monitoring
from models.agent_models import RetrievedChunk, AgentQuery
from services.qdrant_service import qdrant_service
from services.retrieval_service import retrieval_service
from api.models import AgentQueryRequest, AgentQueryResponse, SourceReference


class RAGAgent:
    """
    RAG Agent that handles queries and retrieves relevant context from Qdrant
    """

    def __init__(self):
        self.logger = logger

    async def query(self, request: AgentQueryRequest) -> AgentQueryResponse:
        """
        Process a query request and return a response with relevant context

        Args:
            request: The query request with parameters

        Returns:
            AgentQueryResponse with the response and source references
        """
        start_time = time.time()

        # Log query if enabled
        if monitoring.get("log_queries", True):
            self.logger.info(f"Processing query: '{request.query[:50]}...'")
            self.logger.debug(f"Query request details: scope={request.scope}, max_results={request.max_results}, min_similarity={request.min_similarity}")

        # Performance monitoring
        if monitoring.get("log_performance", True):
            self.logger.info(f"Query started at {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time))}")

        try:
            # Retrieve relevant context from Qdrant
            retrieved_chunks = await self._retrieve_context(
                query_text=request.query,
                scope=request.scope,
                scope_filters=request.scope_filters,
                top_k=request.max_results
            )

            # Generate response using the retrieved context
            response_text = await self._generate_response_with_context(
                query_text=request.query,
                retrieved_chunks=retrieved_chunks
            )

            # Calculate query time
            query_time = time.time() - start_time

            # Create source references
            sources = [
                SourceReference(
                    content=chunk.content,
                    source_url=chunk.source_url,
                    source_title=chunk.source_title,
                    similarity_score=chunk.similarity_score,
                    metadata=chunk.metadata,
                    chunk_id=chunk.id
                )
                for chunk in retrieved_chunks
            ]

            # Calculate confidence using the new method
            confidence = self.calculate_confidence_score(retrieved_chunks)

            # Create and return response
            response = AgentQueryResponse(
                response=response_text,
                sources=sources,
                confidence=confidence,
                query_time=query_time,
                retrieved_chunks_count=len(retrieved_chunks)
            )

            # Performance monitoring
            if monitoring.get("log_performance", True):
                self.logger.info(f"Query processed successfully in {query_time:.2f}s, {len(retrieved_chunks)} chunks used")

                # Check performance threshold
                threshold_ms = monitoring.get("performance_threshold_ms", 2000)
                if query_time * 1000 > threshold_ms:
                    self.logger.warning(f"Query performance exceeded threshold: {query_time*1000:.2f}ms > {threshold_ms}ms")

            # Log query completion if enabled
            if monitoring.get("log_queries", True):
                self.logger.info(f"Query completed successfully in {query_time:.2f}s, {len(retrieved_chunks)} chunks used")

            return response

        except Exception as e:
            query_time = time.time() - start_time
            self.logger.error(f"Error processing query: {e}", exc_info=True)

            # Log error details if enabled
            if monitoring.get("log_queries", True):
                self.logger.error(f"Query failed after {query_time:.2f}s: {str(e)}")

            # Return error response
            return AgentQueryResponse(
                response="An error occurred while processing your query. Please try again later.",
                sources=[],
                confidence=0.0,
                query_time=query_time,
                retrieved_chunks_count=0
            )

    async def _retrieve_context(
        self,
        query_text: str,
        scope: str,
        scope_filters: Optional[Dict[str, Any]],
        top_k: int
    ) -> List[RetrievedChunk]:
        """
        Retrieve relevant context from Qdrant based on the query and scope

        Args:
            query_text: The query text to search for
            scope: The scope of the query (full_book or selected_text)
            scope_filters: Filters to apply based on scope
            top_k: Number of results to retrieve

        Returns:
            List of retrieved chunks
        """
        start_time = time.time()
        try:
            self.logger.debug(f"Starting context retrieval for query with scope '{scope}'")

            # Use OpenAI's embedding API to convert the query_text to a vector
            import openai
            openai.api_key = settings.openai_api_key

            response = await openai.embeddings.create(
                input=query_text,
                model="text-embedding-ada-002"
            )
            query_embedding = response.data[0].embedding

            # Use the retrieval service to get context with scope
            retrieved_chunks = retrieval_service.retrieve_context_with_scope(
                query_embedding=query_embedding,
                scope=scope,
                scope_filters=scope_filters,
                top_k=top_k
            )

            retrieval_time = time.time() - start_time
            self.logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query with scope '{scope}' in {retrieval_time:.2f}s")

            # Log performance metrics if enabled
            if monitoring.get("log_performance", True):
                threshold_ms = monitoring.get("performance_threshold_ms", 2000)
                if retrieval_time * 1000 > threshold_ms:
                    self.logger.warning(f"Context retrieval exceeded threshold: {retrieval_time*1000:.2f}ms > {threshold_ms}ms")

            return retrieved_chunks

        except Exception as e:
            retrieval_time = time.time() - start_time
            self.logger.error(f"Error retrieving context after {retrieval_time:.2f}s: {e}", exc_info=True)
            return []

    async def _generate_response_with_context(
        self,
        query_text: str,
        retrieved_chunks: List[RetrievedChunk]
    ) -> str:
        """
        Generate a response using the query and retrieved context

        Args:
            query_text: The original query
            retrieved_chunks: Chunks of context retrieved from Qdrant

        Returns:
            Generated response text
        """
        start_time = time.time()
        try:
            self.logger.debug(f"Starting response generation with {len(retrieved_chunks)} chunks")

            if not retrieved_chunks:
                response = "I couldn't find any relevant information in the book to answer your query. Please try rephrasing your question."
                self.logger.warning("No relevant chunks found for query")
                return response

            # Combine the content from retrieved chunks to form the context
            context_text = "\n\n".join([chunk.content for chunk in retrieved_chunks])

            # Create a prompt for OpenAI with the query and context
            prompt = f"""
            You are a helpful assistant that answers questions based on the provided book content.
            Please answer the following question using only the information provided in the context below.
            If the answer cannot be found in the context, say so clearly.

            Question: {query_text}

            Context:
            {context_text}

            Answer:
            """

            # Use OpenAI's API to generate the response
            import openai
            openai.api_key = settings.openai_api_key

            response = await openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context. Answer accurately and cite sources when possible."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )

            # Extract the generated response
            generated_response = response.choices[0].message.content.strip()

            # Add source citations to the response
            if retrieved_chunks:
                generated_response += f"\n\nSources used ({len(retrieved_chunks)} chunks):"
                for i, chunk in enumerate(retrieved_chunks[:3]):  # Cite top 3 sources
                    generated_response += f"\n{i+1}. {chunk.source_title} ({chunk.source_url}) - Similarity: {chunk.similarity_score:.2f}"

            generation_time = time.time() - start_time
            self.logger.info(f"Response generated successfully in {generation_time:.2f}s")

            # Log performance metrics if enabled
            if monitoring.get("log_performance", True):
                threshold_ms = monitoring.get("performance_threshold_ms", 2000)
                if generation_time * 1000 > threshold_ms:
                    self.logger.warning(f"Response generation exceeded threshold: {generation_time*1000:.2f}ms > {threshold_ms}ms")

            return generated_response

        except Exception as e:
            generation_time = time.time() - start_time
            self.logger.error(f"Error generating response after {generation_time:.2f}s: {e}", exc_info=True)
            return "An error occurred while generating the response. Please try again later."

    def calculate_confidence_score(self, retrieved_chunks: List[RetrievedChunk]) -> float:
        """
        Calculate an overall confidence score based on the retrieved chunks

        Args:
            retrieved_chunks: List of retrieved chunks

        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not retrieved_chunks:
            return 0.0

        # Calculate average similarity score
        avg_similarity = sum(chunk.similarity_score for chunk in retrieved_chunks) / len(retrieved_chunks)

        # Calculate confidence based on number of chunks and their similarity
        num_chunks_factor = min(len(retrieved_chunks) / 5.0, 1.0)  # Up to 1.0 for 5+ chunks
        similarity_factor = avg_similarity

        # Combine factors for overall confidence
        confidence = (similarity_factor * 0.7) + (num_chunks_factor * 0.3)

        return min(confidence, 1.0)  # Cap at 1.0


# Global instance
rag_agent = RAGAgent()