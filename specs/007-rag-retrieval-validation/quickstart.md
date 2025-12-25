# Quickstart Guide: RAG Retrieval Validation

## Overview
This guide provides a quick introduction to setting up and using the RAG retrieval validation system. The system allows you to query a Qdrant vector database with natural language queries and validate the retrieval accuracy of your RAG pipeline.

## Prerequisites
- Python 3.11+
- Access to Qdrant Cloud instance
- Cohere API key
- (Optional) Docker for containerized deployment

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set Up Environment
```bash
cd backend_rag_pipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the `backend_rag_pipeline` directory:
```env
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
```

## Basic Usage

### 1. Run the Validation Service
```bash
cd backend_rag_pipeline
python main.py
```

### 2. Query the Vector Database
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "query_text": "What is ROS 2?",
    "top_k": 5,
    "metadata_filters": {
      "module": "Module 1"
    }
  }'
```

### 3. Validate Retrieval Accuracy
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "validation_queries": [
      {
        "query": "What is the difference between ROS 1 and ROS 2?",
        "expected_answers": ["decentralized architecture", "DDS", "improved security"]
      }
    ]
  }'
```

## Configuration Options

### Environment Variables
- `QDRANT_URL`: URL of your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant Cloud
- `COHERE_API_KEY`: API key for Cohere services
- `API_PORT`: Port for the validation service (default: 8000)
- `API_HOST`: Host for the validation service (default: localhost)
- `DEFAULT_TOP_K`: Default number of results to return (default: 5)

### Runtime Parameters
- `--top_k`: Number of top results to return per query
- `--similarity_threshold`: Minimum similarity score for results
- `--validation_threshold`: Minimum accuracy threshold for validation

## Validation Test Suite
The system includes a pre-built validation test suite with common book-related queries:

1. **Core Concepts**: Tests retrieval of fundamental concepts from the book
2. **Module-Specific Queries**: Validates retrieval within specific book modules
3. **Cross-Module Queries**: Tests retrieval across multiple book modules
4. **Metadata Filtering**: Validates that metadata filters work correctly

Run the full test suite:
```bash
python -m pytest tests/validation_test_suite.py -v
```

## Troubleshooting

### Common Issues
1. **Connection Errors**: Verify QDRant URL and API key are correct
2. **Authentication Errors**: Check Cohere API key is valid and has proper permissions
3. **Slow Queries**: Verify Qdrant Cloud instance has sufficient resources
4. **Empty Results**: Check that the vector database contains relevant content

### Performance Tips
- Use metadata filters to narrow down search scope
- Adjust `top_k` parameter based on your needs
- Monitor Qdrant Cloud instance performance metrics
- Consider caching frequent queries for better performance

## Next Steps
1. Customize the validation queries for your specific use case
2. Integrate with your existing RAG pipeline
3. Set up monitoring and alerting for the validation service
4. Add more test cases to the validation suite