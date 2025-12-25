import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test the API keys
cohere_api_key = os.getenv("COHERE_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

logger.info(f"Cohere API Key loaded: {bool(cohere_api_key)}")
logger.info(f"Qdrant URL loaded: {bool(qdrant_url)}")
logger.info(f"Qdrant API Key loaded: {bool(qdrant_api_key)}")

if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required")
if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

logger.info("All environment variables are properly loaded. Ready to run the full pipeline.")