from fastapi import FastAPI, HTTPException, Query
from typing import Optional, Dict, Any, List
import time
import logging

from retrieval_validation.models import QueryRequest, RetrievalResult, ValidationResult
from retrieval_validation.query_processor import query_processor
from retrieval_validation.qdrant_client import qdrant_client
from retrieval_validation.validation_engine import validation_engine

logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Retrieval Validation API",
    description="API for validating RAG retrieval accuracy and similarity",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """
    Root endpoint to verify API is running
    """
    return {"message": "RAG Retrieval Validation API is running"}

@app.post("/search", response_model=RetrievalResult)
def search_chunks(request: QueryRequest):
    """
    Search for relevant content chunks based on the query
    """
    start_time = time.time()
    logger.info(f"Search request received with query: '{request.query_text[:50]}...' and top_k: {request.top_k}")

    try:
        # Validate input parameters
        validated_params = query_processor.validate_query_input(
            request.query_text,
            request.top_k,
            request.similarity_threshold
        )

        # Convert query to embedding
        logger.debug("Converting query to embedding")
        query_embedding = query_processor.convert_query_to_embedding(validated_params["query_text"])

        # Perform similarity search
        logger.debug("Performing similarity search in Qdrant")
        retrieved_chunks = qdrant_client.search_similar_chunks(
            query_embedding=query_embedding,
            top_k=validated_params["top_k"],
            metadata_filters=request.metadata_filters
        )

        # Filter by similarity threshold if provided
        initial_count = len(retrieved_chunks)
        if validated_params["similarity_threshold"] is not None:
            retrieved_chunks = [
                chunk for chunk in retrieved_chunks
                if chunk.similarity_score >= validated_params["similarity_threshold"]
            ]
            logger.info(f"Applied similarity threshold filter: {initial_count} -> {len(retrieved_chunks)} chunks")

        execution_time = time.time() - start_time
        logger.info(f"Search completed in {execution_time:.2f}s, returned {len(retrieved_chunks)} chunks")

        # Create search parameters dict
        search_params = {
            "top_k": str(validated_params["top_k"]),
            "similarity_threshold": str(validated_params["similarity_threshold"]) if validated_params["similarity_threshold"] is not None else "None"
        }

        if request.metadata_filters:
            search_params["metadata_filters"] = str(request.metadata_filters)

        # Create and return retrieval result
        result = RetrievalResult(
            query_request=request,
            retrieved_chunks=retrieved_chunks,
            execution_time=execution_time,
            total_chunks_found=len(retrieved_chunks),
            search_params=search_params
        )

        return result

    except ValueError as ve:
        execution_time = time.time() - start_time
        logger.error(f"Validation error in search after {execution_time:.2f}s: {ve}")
        raise HTTPException(status_code=400, detail=f"Validation error: {str(ve)}")
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error in search operation after {execution_time:.2f}s: {e}")
        raise HTTPException(status_code=500, detail=f"Search operation failed: {str(e)}")

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify system components are operational
    """
    try:
        # Test basic connectivity by attempting a simple operation
        # For now, just return success - in a real implementation you might
        # test connectivity to Qdrant and Cohere APIs
        return {
            "status": "healthy",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Health check failed")

@app.post("/validate", response_model=ValidationResult)
def validate_single_query(
    query: str = Query(..., description="The query to validate"),
    expected_answers: List[str] = Query(..., description="Expected answers for validation"),
    top_k: int = Query(5, description="Number of top results to retrieve"),
    threshold: float = Query(0.7, description="Minimum accuracy threshold")
):
    """
    Validate retrieval accuracy for a single query against expected answers
    """
    start_time = time.time()
    logger.info(f"Validation request received for query: '{query[:50]}...' with {len(expected_answers)} expected answers")

    try:
        # Create a search function to pass to the validation engine
        def search_function(search_query: str):
            logger.debug(f"Validating search query: {search_query[:30]}...")
            # Validate input parameters
            validated_params = query_processor.validate_query_input(
                search_query,
                top_k
            )

            # Convert query to embedding
            query_embedding = query_processor.convert_query_to_embedding(validated_params["query_text"])

            # Perform similarity search
            retrieved_chunks = qdrant_client.search_similar_chunks(
                query_embedding=query_embedding,
                top_k=validated_params["top_k"]
            )

            logger.debug(f"Search returned {len(retrieved_chunks)} chunks for validation")
            return retrieved_chunks

        # Perform search
        retrieved_chunks = search_function(query)

        # Validate the results
        result = validation_engine.validate_retrieval_accuracy(
            query=query,
            expected_answers=expected_answers,
            retrieved_chunks=retrieved_chunks,
            threshold=threshold
        )

        execution_time = time.time() - start_time
        logger.info(f"Validation completed in {execution_time:.2f}s with accuracy score: {result.accuracy_score:.2f}")

        return result

    except ValueError as ve:
        execution_time = time.time() - start_time
        logger.error(f"Validation error after {execution_time:.2f}s: {ve}")
        raise HTTPException(status_code=400, detail=f"Validation error: {str(ve)}")
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error in validation operation after {execution_time:.2f}s: {e}")
        raise HTTPException(status_code=500, detail=f"Validation operation failed: {str(e)}")


@app.post("/validate-suite")
def validate_test_suite(
    test_queries: List[Dict[str, Any]]
):
    """
    Run a comprehensive validation test suite
    """
    start_time = time.time()
    logger.info(f"Validation suite request received with {len(test_queries)} test queries")

    try:
        # Convert test queries to the expected format: List[Tuple[str, List[str]]]
        formatted_queries = []
        for i, test_query in enumerate(test_queries):
            query = test_query.get("query", "")
            expected_answers = test_query.get("expected_answers", [])
            formatted_queries.append((query, expected_answers))
            logger.debug(f"Formatted test query {i+1}: '{query[:30]}...' with {len(expected_answers)} expected answers")

        # Create a search function to pass to the validation engine
        def search_function(search_query: str):
            logger.debug(f"Running search for validation suite: {search_query[:30]}...")
            # Use default parameters for the search
            validated_params = query_processor.validate_query_input(
                search_query,
                5  # default top_k
            )

            # Convert query to embedding
            query_embedding = query_processor.convert_query_to_embedding(validated_params["query_text"])

            # Perform similarity search
            retrieved_chunks = qdrant_client.search_similar_chunks(
                query_embedding=query_embedding,
                top_k=validated_params["top_k"]
            )

            logger.debug(f"Search returned {len(retrieved_chunks)} chunks for validation suite")
            return retrieved_chunks

        # Run the validation test suite
        results = validation_engine.run_validation_test_suite(
            test_queries=formatted_queries,
            search_function=search_function
        )

        execution_time = time.time() - start_time
        logger.info(f"Validation suite completed in {execution_time:.2f}s. "
                   f"Pass rate: {results['pass_rate']:.2f}, "
                   f"Overall accuracy: {results['overall_accuracy']:.2f}")

        return results

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error in validation suite operation after {execution_time:.2f}s: {e}")
        raise HTTPException(status_code=500, detail=f"Validation suite operation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT

    uvicorn.run(app, host=API_HOST, port=API_PORT)