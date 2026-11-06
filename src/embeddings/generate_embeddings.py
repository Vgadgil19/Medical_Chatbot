import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

#Load path
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from langchain_openai import OpenAIEmbeddings
from src.preprocessing.split_documents import chunks

#Define Embedding model
model = OpenAIEmbeddings(model="text-embedding-3-small")


texts = [chunk.page_content for chunk in chunks]

print("Sending request to OpenAI...")

all_embeddings = model.embed_documents(texts)

print("Embedding generated successfully!")

print("Total embeddings generated:", len(all_embeddings))
print("Dimensions:", len(all_embeddings[0]))