import sys
from pathlib import Path
from dotenv import load_dotenv

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Add project root to Python path
sys.path.append(str(BASE_DIR))

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_classic.retrievers import MultiQueryRetriever

model = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name="langchain",
    embedding_function=model,
    persist_directory=str(BASE_DIR/"src"/"embeddings"/"vector_db")
)

ret = MultiQueryRetriever.from_llm(
    retriever = vector_store.as_retriever(search_kwargs = {"k":3}),
    llm = ChatOpenAI(model = "gpt-4.1-mini")
)


# query = "What are symptoms of diebates?"

# docs = ret.invoke(query)

# for i, ind in enumerate(docs, start=1):
#     print(f"Result {i}")
#     print("Title : ",ind.metadata.get("title"))
#     print("URL : ",ind.metadata.get("url"))
#     print("Content : ", ind.page_content)
if __name__ == "__main__":

    query = "What are symptoms of diabetes?"

    docs = ret.invoke(query)

    for i, doc in enumerate(docs, start=1):
        print(f"\nResult {i}")
        print("Title:", doc.metadata.get("title"))
        print("URL:", doc.metadata.get("url"))
        print("Content:", doc.page_content)