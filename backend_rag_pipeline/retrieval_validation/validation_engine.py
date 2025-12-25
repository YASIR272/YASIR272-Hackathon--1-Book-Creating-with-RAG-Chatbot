import logging
from typing import List, Dict, Tuple
from retrieval_validation.models import RetrievedChunk, ValidationResult
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from retrieval_validation.query_processor import QueryProcessor

logger = logging.getLogger(__name__)

class ValidationEngine:
    """
    Engine for validating retrieval accuracy and providing feedback
    """

    def __init__(self):
        """
        Initialize the validation engine
        """
        self.query_processor = QueryProcessor()

    def calculate_similarity_score(self, text1: str, text2: str) -> float:
        """
        Calculate similarity score between two text chunks using embeddings
        This is a simplified version - in practice, you might use more sophisticated methods
        """
        try:
            # For now, we'll use a simple text similarity approach
            # In a real implementation, we would use embeddings to calculate similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())

            if not words1 and not words2:
                return 1.0  # Both empty, perfectly similar
            if not words1 or not words2:
                return 0.0  # One empty, not similar

            intersection = words1.intersection(words2)
            union = words1.union(words2)

            jaccard_similarity = len(intersection) / len(union)
            return jaccard_similarity
        except Exception as e:
            logger.error(f"Error calculating similarity score: {e}")
            return 0.0

    def validate_retrieval_accuracy(
        self,
        query: str,
        expected_answers: List[str],
        retrieved_chunks: List[RetrievedChunk],
        threshold: float = 0.7
    ) -> ValidationResult:
        """
        Validate retrieval accuracy against expected answers

        Args:
            query: The original query
            expected_answers: List of expected answer texts
            retrieved_chunks: List of retrieved chunks from search
            threshold: Minimum accuracy score to pass validation

        Returns:
            ValidationResult containing accuracy metrics
        """
        try:
            if not retrieved_chunks:
                return ValidationResult(
                    query=query,
                    expected_answers=expected_answers,
                    retrieved_chunks=retrieved_chunks,
                    accuracy_score=0.0,
                    validation_passed=False,
                    detailed_feedback="No chunks retrieved for the query"
                )

            # Calculate similarity between expected answers and retrieved chunks
            total_score = 0.0
            max_possible_score = 0.0

            for expected_answer in expected_answers:
                best_chunk_score = 0.0

                for chunk in retrieved_chunks:
                    chunk_score = self.calculate_similarity_score(expected_answer, chunk.content)
                    best_chunk_score = max(best_chunk_score, chunk_score)

                total_score += best_chunk_score
                max_possible_score += 1.0  # Max possible score per expected answer is 1.0

            # Calculate average accuracy score
            accuracy_score = total_score / len(expected_answers) if expected_answers else 0.0

            # Determine if validation passed
            validation_passed = accuracy_score >= threshold

            # Generate detailed feedback
            feedback_parts = []
            if accuracy_score < threshold:
                feedback_parts.append(f"Accuracy score {accuracy_score:.2f} is below threshold {threshold}")
            else:
                feedback_parts.append(f"Accuracy score {accuracy_score:.2f} meets threshold {threshold}")

            if retrieved_chunks:
                feedback_parts.append(f"Retrieved {len(retrieved_chunks)} chunks")
            else:
                feedback_parts.append("No chunks retrieved")

            detailed_feedback = "; ".join(feedback_parts)

            return ValidationResult(
                query=query,
                expected_answers=expected_answers,
                retrieved_chunks=retrieved_chunks,
                accuracy_score=accuracy_score,
                validation_passed=validation_passed,
                detailed_feedback=detailed_feedback
            )

        except Exception as e:
            logger.error(f"Error validating retrieval accuracy: {e}")
            return ValidationResult(
                query=query,
                expected_answers=expected_answers,
                retrieved_chunks=retrieved_chunks,
                accuracy_score=0.0,
                validation_passed=False,
                detailed_feedback=f"Error during validation: {str(e)}"
            )

    def run_validation_test_suite(
        self,
        test_queries: List[Tuple[str, List[str]]],  # (query, expected_answers)
        search_function  # Function to perform search
    ) -> Dict[str, any]:
        """
        Run a comprehensive validation test suite

        Args:
            test_queries: List of (query, expected_answers) tuples
            search_function: Function to perform search operations

        Returns:
            Dictionary with validation metrics and results
        """
        try:
            total_tests = len(test_queries)
            passed_tests = 0
            validation_results = []
            total_accuracy = 0.0

            for query, expected_answers in test_queries:
                # Perform search
                retrieved_chunks = search_function(query)

                # Validate the results
                result = self.validate_retrieval_accuracy(
                    query=query,
                    expected_answers=expected_answers,
                    retrieved_chunks=retrieved_chunks
                )

                validation_results.append(result)
                total_accuracy += result.accuracy_score

                if result.validation_passed:
                    passed_tests += 1

            overall_accuracy = total_accuracy / total_tests if total_tests > 0 else 0.0
            pass_rate = passed_tests / total_tests if total_tests > 0 else 0.0

            return {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "overall_accuracy": overall_accuracy,
                "pass_rate": pass_rate,
                "validation_results": validation_results
            }

        except Exception as e:
            logger.error(f"Error running validation test suite: {e}")
            raise

# Global instance for use throughout the application
validation_engine = ValidationEngine()