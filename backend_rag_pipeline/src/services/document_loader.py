"""
Document Loader Service for RAG Chatbot Integration
Loads and processes book content for retrieval
"""

import os
import re
from typing import List, Dict, Any
from pathlib import Path


class DocumentLoader:
    """
    Service to load and process documents from the book content
    """

    def __init__(self, docs_path: str = "E:/Hackathon Complete Project 1 Booking Creation/frontend_book/docs"):
        self.docs_path = Path(docs_path)
        self.documents = []
        self.processed_docs = {}

    def load_documents(self) -> List[Dict[str, Any]]:
        """
        Load all markdown documents from the book
        """
        if self.documents:
            return self.documents

        docs_dir = Path(self.docs_path)
        markdown_files = docs_dir.rglob("*.md")

        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Extract title from the first heading
                    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                    title = title_match.group(1) if title_match else file_path.stem

                    # Create document object
                    doc = {
                        'id': str(file_path.relative_to(self.docs_path)),
                        'title': title,
                        'content': content,
                        'path': str(file_path),
                        'url': self._get_url_from_path(file_path)
                    }

                    self.documents.append(doc)
                    self.processed_docs[doc['id']] = doc

            except Exception as e:
                print(f"Error loading document {file_path}: {e}")

        return self.documents

    def _get_url_from_path(self, file_path: Path) -> str:
        """
        Convert file path to a URL relative to the docs directory
        """
        relative_path = file_path.relative_to(Path(self.docs_path))
        # Convert to URL format (e.g., module1/chapter1-fundamentals.md -> /docs/module1/chapter1-fundamentals)
        url_path = str(relative_path).replace('.md', '').replace('\\', '/')
        return f"/docs/{url_path}"

    def search_documents(self, query: str, selected_text: str = None) -> List[Dict[str, Any]]:
        """
        Simple search implementation - in a real system, this would use embeddings
        For now, we'll do keyword matching
        """
        if not self.documents:
            self.load_documents()

        results = []
        search_terms = (query + " " + (selected_text or "")).lower().split()

        for doc in self.documents:
            content_lower = doc['content'].lower()
            title_lower = doc['title'].lower()

            # Calculate a simple relevance score
            score = 0
            for term in search_terms:
                if term in title_lower:
                    score += 2  # Title matches are more important
                if term in content_lower:
                    score += 1  # Content matches

            if score > 0:
                # Extract relevant text snippets
                relevant_snippets = self._extract_relevant_snippets(content_lower, search_terms, doc['content'])

                results.append({
                    'document_id': doc['id'],
                    'title': doc['title'],
                    'url': doc['url'],
                    'content': doc['content'],
                    'relevance_score': score,
                    'snippets': relevant_snippets
                })

        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)

        # Return top 5 results
        return results[:5]

    def _extract_relevant_snippets(self, content_lower: str, search_terms: List[str], original_content: str) -> List[str]:
        """
        Extract relevant text snippets that contain search terms
        """
        snippets = []

        # Split content into paragraphs
        paragraphs = re.split(r'\n\s*\n', original_content)

        for paragraph in paragraphs:
            para_lower = paragraph.lower()
            if any(term in para_lower for term in search_terms):
                # Limit snippet to 200 characters
                snippet = paragraph[:200] + ("..." if len(paragraph) > 200 else "")
                snippets.append(snippet)

                # Limit to 3 snippets
                if len(snippets) >= 3:
                    break

        return snippets


# Global document loader instance
document_loader = DocumentLoader()