# Quickstart Guide: Book Content RAG Pipeline

## Prerequisites

- Python 3.11 or higher
- pip package manager
- UV package manager (optional, but recommended as specified)

## Setup

### 1. Clone or Create the Project Directory

```bash
mkdir backend_rag_pipeline
cd backend_rag_pipeline
```

### 2. Create Virtual Environment and Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or use UV (as specified in requirements)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Create requirements.txt

```txt
requests==2.31.0
beautifulsoup4==4.12.2
cohere==4.4.3
qdrant-client==1.7.0
python-dotenv==1.0.0
lxml==4.9.3
pytest==7.4.3
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
# Or with UV:
uv pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the project root:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
BOOK_URL=https://frontendbook-theta.vercel.app/
```

## Usage

### Run the Complete Pipeline

```bash
python main.py
```

The main function will execute the complete pipeline:
1. Get all URLs from the specified book site
2. Extract text content from each URL
3. Chunk the content with metadata
4. Generate embeddings using Cohere
5. Create the 'book_embedding' collection in Qdrant
6. Save all chunks to Qdrant

### Run Individual Components (for testing)

You can also run individual functions for testing and development:

```python
# Example of using individual functions:
from main import get_all_urls, extract_text_from_url, chunk_text, embed, create_collection, save_chunk_to_qdrant

# Get all URLs from the book
urls = get_all_urls("https://frontendbook-theta.vercel.app/")

# Extract content from a specific URL
content = extract_text_from_url(urls[0])

# Chunk the content
chunks = chunk_text(content, urls[0], "Sample Title")

# Generate embeddings
embedded_chunks = []
for chunk in chunks:
    embedding = embed(chunk['content'])
    embedded_chunks.append({
        'chunk': chunk,
        'embedding': embedding
    })
```

## Testing

Run the tests to verify functionality:

```bash
pytest tests/
```

Or run specific tests:

```bash
pytest tests/test_main.py -v
```

## Configuration

The pipeline can be configured through environment variables in the `.env` file:

- `BOOK_URL`: The base URL of the Docusaurus book to crawl (default: https://frontendbook-theta.vercel.app/)
- `COHERE_API_KEY`: Your Cohere API key for generating embeddings
- `QDRANT_URL`: Your Qdrant Cloud cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `CHUNK_SIZE`: Maximum size of text chunks (default: 1000 characters)
- `CHUNK_OVERLAP`: Overlap between chunks to maintain context (default: 100 characters)