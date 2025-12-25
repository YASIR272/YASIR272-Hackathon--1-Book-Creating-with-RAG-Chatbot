"""
Query Processing Service for RAG Chatbot Integration
Handles the processing of user queries and generation of responses
"""

import asyncio
from typing import List, Tuple
from ..models.source_reference import SourceReference
from .document_loader import document_loader


class QueryProcessor:
    """
    Service class to process user queries and generate responses from RAG system
    """

    def __init__(self):
        """
        Initialize the query processor
        """
        # Load documents for the knowledge base
        document_loader.load_documents()

    async def process_query(self, query_text: str, selected_text: str = None) -> Tuple[str, List[SourceReference]]:
        """
        Process a user query and return a response with sources

        Args:
            query_text: The user's query
            selected_text: Optional selected text context

        Returns:
            A tuple of (response_text, list_of_sources)
        """
        # Search for relevant documents
        search_results = document_loader.search_documents(query_text, selected_text)

        # Generate response based on found documents
        response_text = self._generate_response(query_text, selected_text, search_results)

        # Create source references from search results
        sources = self._generate_sources(search_results)

        return response_text, sources

    def _generate_response(self, query_text: str, selected_text: str, search_results: List[dict]) -> str:
        """
        Generate a response based on query and search results
        """
        if not search_results:
            return f"I couldn't find specific information about '{query_text[:50]}{'...' if len(query_text) > 50 else ''}' in the book content. Please try rephrasing your question or check the book modules for relevant information."

        # Build response from the most relevant documents
        response_parts = [
            f"Based on the book content, here's information about '{query_text[:50]}{'...' if len(query_text) > 50 else ''}':"
        ]

        # Add information from the most relevant documents
        for i, result in enumerate(search_results[:2]):  # Use top 2 results
            response_parts.append(f"\nFrom '{result['title']}':")
            if result['snippets']:
                for snippet in result['snippets'][:2]:  # Use top 2 snippets
                    response_parts.append(f"- {snippet}")
            else:
                # If no snippets, use first 100 chars of content
                content_preview = result['content'][:100] + ("..." if len(result['content']) > 100 else "")
                response_parts.append(f"- {content_preview}")

        if selected_text:
            response_parts.append(f"\n\nThe selected text context: '{selected_text[:100]}{'...' if len(selected_text) > 100 else ''}'")

        response_parts.append("\n\nThis information is based on the book's content. For more details, check the referenced sections.")

        return " ".join(response_parts)

    def _generate_sources(self, search_results: List[dict]) -> List[SourceReference]:
        """
        Generate source references from search results
        """
        sources = []

        for result in search_results:
            # Create a source reference for the main document
            sources.append(SourceReference(
                document_id=result['document_id'],
                section=result['title'],
                page_url=result['url'],
                text=result['snippets'][0] if result['snippets'] else result['content'][:200] + ("..." if len(result['content']) > 200 else ""),
                confidence=min(1.0, result['relevance_score'] / 10.0)  # Normalize relevance score to 0-1 range
            ))

        return sources

    def validate_query(self, query_text: str) -> bool:
        """
        Validate that the query is appropriate for processing
        """
        if not query_text or len(query_text.strip()) == 0:
            return False

        if len(query_text) > 1000:
            return False

        return True