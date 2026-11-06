import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

json_path = BASE_DIR/"data"/"processed"/"medical_data.json"

with open(json_path, "r", encoding="utf-8") as file:
    medical_data = json.load(file)
print("total medical records loaded : ", len(medical_data))

from langchain_core.documents import Document

# record = medical_data[0]

# doc = Document(
#     page_content=record["summary"],
#     metadata = {
#         "title" : record["title"],
#         "url" : record["url"],
#         "id" : record["id"]
#     }
# )

# #print(doc)
# print(type(doc))
# print(type(doc.page_content))
# print(type(doc.metadata))

documents = []

for record in medical_data:
    doc = Document(
     page_content = record["summary"],
    metadata = {
        "title" : record["title"],
        "url" : record["url"],
        "id" : record["id"]
    } 
    )
    documents.append(doc)
print("total langchain records loaded : ", len(documents))

empty_docs = [
    doc for doc in documents
    if not doc.page_content.strip()
]

# print("length of empty docs : ", len(empty_docs))

# for doc in empty_docs:
#     print("Title : ", doc.metadata["title"])
#     print("URL : ", doc.metadata["url"])
    
valid_documents = [
    doc for doc in documents
    if doc.page_content.strip()
]

print("length of valid docs : ", len(valid_documents))