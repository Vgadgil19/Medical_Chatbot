# import xml.etree.ElementTree as ET
# from pathlib import Path

# file_path = Path("data/raw/medilineplus/health_topics.xml")

# if not file_path:
#     raise FileNotFoundError(f"Dataset not found!: {file_path.resolve()}")

# tree = ET.parse(file_path)
# root = tree.getroot()

# print("XML loaded successfully!")
# print("Root element:", root.tag)
# print("Root attributes:", root.attrib) 


import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup

# Get the project root directory (Medical_Chatbot)
BASE_DIR = Path(__file__).resolve().parents[2]

# Define the XML dataset path
file_path = (
    BASE_DIR
    / "data"
    / "raw"
    / "medilineplus"
    / "health_topics.xml"
)

# Check if the dataset exists
if not file_path.exists():
    raise FileNotFoundError(
        f"Dataset not found: {file_path.resolve()}"
    )

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

print("XML loaded successfully!")
print("Root element:", root.tag)
print("Root attributes:", root.attrib)

# Inspect the first-level child elements
print("\n--- XML Structure ---")

# for child in root:
#     print("Tag:", child.tag)
#     print("Attributes:", child.attrib)
#     print("-" * 50)

# # Identify health-topic records
# all_records = [
#     element
#     for element in root.iter()
#     if element.tag.split("}")[-1] == "health-topic"
# ]

# print("\nTotal medical records:", len(all_records))

# # Display the first record
# if all_records:
#     print("\n--- First Medical Record ---")
#     print(ET.tostring(all_records[0], encoding="unicode"))
# else:
#     print("No health-topic records found.")


# Identify all health-topic records
all_records = [
    element
    for element in root.iter()
    if element.tag.split("}")[-1] == "health-topic"
]

print("Total records:", len(all_records))

# Keep only English records
english_records = [
    record
    for record in all_records
    if record.attrib.get("language", "").strip().lower() == "english"
]

print("English records:", len(english_records))

# Count records in other languages
other_records = len(all_records) - len(english_records)

print("Non-English records excluded:", other_records)

# medical_data = []

# for record in english_records:
    
#     summary_ele = record.find("full-summary")
    
#     summary_text = ""
    
#     if summary_ele is not None and summary_ele.text:
#         soup = BeautifulSoup(summary_ele.text, "html.parser")
#         summary_text = soup.get_text(separator=" ",strip=True)
    
#     data = {
#         "title": record.attrib.get("title", "").strip(),
#         "description" : record.attrib.get("meta-desc", "").strip(),
#         "url" : record.attrib.get("url", "").strip(),
#         "id" : record.attrib.get("id", "").strip(),
#         "date_created" : record.attrib.get("date-created", "").strip(),
#         "summary" : summary_text
#     }
    
#     medical_data.append(data)

# print("\n Medical data extraction and cleaning completed")
# print("\n length of medical records : ", len(medical_data))

# empty_summaries = sum(
#     1 for data in medical_data
#     if not data["summary"]
# )

# print("Records with empty summaries:", empty_summaries)

# for data in medical_data:
#     if not data["summary"]:
#         print("Title:", data["title"])
#         print("ID:", data["id"])
#         print("URL:", data["url"])

# for index,data in enumerate(medical_data[:3],start=1):
#     print(f"medical record {index}")
#     for key, value in data.items():
#         print(f"{key}:{value}")

# for data in medical_data[:3]:
#     print("\nTitle:", data["title"])
#     print("Summary:", data["summary"][:500])


# Inspect the complete structure of the first English record

# if english_records:
#     first_record = english_records[0]

#     print("\n--- Complete XML Record ---")

#     print(
#         ET.tostring(
#             first_record,
#             encoding="unicode"
#         )
#     )
# empty_descriptions = sum(
#     1 for data in medical_data
#     if not data["description"]
# )

# print("Records with empty descriptions:", empty_descriptions)

# summary = first_record.find("full-summary")
# print("\n Full summary")
# print(summary.text)

# Extract medical records
medical_data = []

for record in english_records:

    # Extract full summary
    summary_ele = record.find("full-summary")

    summary_text = ""

    if summary_ele is not None and summary_ele.text:
        soup = BeautifulSoup(summary_ele.text, "html.parser")
        summary_text = soup.get_text(separator=" ", strip=True)

    # Store extracted information
    data = {
        "title": record.attrib.get("title", "").strip(),
        "description": record.attrib.get("meta-desc", "").strip(),
        "url": record.attrib.get("url", "").strip(),
        "id": record.attrib.get("id", "").strip(),
        "date_created": record.attrib.get("date-created", "").strip(),
        "summary": summary_text,
        "has_summary": bool(summary_text)
    }

    medical_data.append(data)


# Display extraction results
print("\nMedical data extraction completed!")
print("Total medical records:", len(medical_data))

# Count records with empty summaries
empty_summaries = sum(
    1 for data in medical_data
    if not data["has_summary"]
)

print("Records with empty summaries:", empty_summaries)

# Identify records with empty summaries
for data in medical_data:
    if not data["has_summary"]:
        print("\nTitle:", data["title"])
        print("ID:", data["id"])
        print("URL:", data["url"])


# # Inspect first three records
# for data in medical_data[:3]:
#     print("\nTitle:", data["title"])
#     print("Summary:", data["summary"][:500])
#     print("Has summary:", data["has_summary"])
    


empty_titles = sum(
    1 for data in medical_data
    if not data["title"]
)

empty_descriptions = sum(
    1 for data in medical_data
    if not data["description"]
)

print("Records with empty titles:", empty_titles)
print("Records with empty descriptions:", empty_descriptions)

# for data in medical_data:
#     if not data["description"]:
#         print("Title:", data["title"])
#         print("ID:", data["id"])
#         print("URL:", data["url"])
        
for data in medical_data:
    if data["id"] == "6055":
        print("Title:", data["title"])
        print("Has Summary? : ", data["has_summary"])
        print("Summary", data["summary"][:500])
        # print("URL: ", data["url"])
        
#

# for record in english_records:
#     if record.attrib.get("title") == "A1C":
        
#         groups = record.findall("group")
#         for group in groups:
#             print(ET.tostring(group,encoding="unicode"))
#         break

# for data in medical_data:
#     if data["title"] == "A1C":
#         print(data["related_topics"])
#         break

# for data in medical_data:
#     if data["has_alt_name"]:
#         print("name : ", data["title"])
#         print("alternative name : ", data["alternative_names"])
