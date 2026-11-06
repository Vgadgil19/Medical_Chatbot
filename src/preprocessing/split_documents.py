import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.preprocessing.create_documents import valid_documents

splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 150)
chunks = splitter.split_documents(valid_documents)

print("Total original documents:", len(valid_documents))
print("Total chunks generated:", len(chunks))

# print("\nSecond chunk:")
# print(chunks[1].page_content)

# print("\nChunk metadata:")
# print(chunks[1].metadata)

# print("\nSecond chunk length:")
# print(len(chunks[1].page_content))

for i in range (3):
    print(f"Chunk{i+1}")
    print("Title", chunks[i].metadata["title"])
    print("ID", chunks[i].metadata["id"])
    print("URL", chunks[i].metadata["url"])