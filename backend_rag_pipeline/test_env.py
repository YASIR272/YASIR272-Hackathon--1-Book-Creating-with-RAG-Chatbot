import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment variables check:")
print(f"COHERE_API_KEY exists: {'COHERE_API_KEY' in os.environ}")
print(f"QDRANT_URL exists: {'QDRANT_URL' in os.environ}")
print(f"QDRANT_API_KEY exists: {'QDRANT_API_KEY' in os.environ}")
print(f"BOOK_URL exists: {'BOOK_URL' in os.environ}")

print(f"\nBOOK_URL value: {os.getenv('BOOK_URL', 'NOT FOUND')}")