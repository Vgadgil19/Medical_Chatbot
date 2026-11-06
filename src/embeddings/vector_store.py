import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

#Load path
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.preprocessing.split_documents import chunks

embedding_model = OpenAIEmbeddings(model = "text-embedding-3-small")

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="vector_db"
)

print("Medical documents stored in ChromaDB successfully!")
print("Total stored chunks:", vector_store._collection.count())