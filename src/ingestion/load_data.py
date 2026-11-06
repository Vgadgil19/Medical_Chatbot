import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup
import json

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


#Extract Medical Records
medical_data = []

for record in english_records:
    
    #alternative names
    also_called = record.findall("also-called")
    
    alternative_names = [
        item.text.strip()
        for item in also_called
        if item.text
    ]
    
    #Summary Extraction
    summary_ele = record.find("full-summary")
    
    summary_text = ""
    
    if summary_ele is not None and summary_ele.text:
        soup = BeautifulSoup(summary_ele.text, "html.parser")
        summary_text = soup.get_text(separator=" ",strip=True)
    
    #Relative topics extraction
    groups = record.findall("group")
    
    relative_topics = [
        {
            "name" : group.text.strip(),
            "url" : group.attrib.get("url","").strip(),
            "id" : group.attrib.get("id", "").strip()
        }
        for group in groups
        if group.text
    ]
    
    #Final Data of each medical records
    data = {
        "title": record.attrib.get("title", "").strip(),
        "description" : record.attrib.get("meta-desc", "").strip(),
        "url" : record.attrib.get("url", "").strip(),
        "id" : record.attrib.get("id", "").strip(),
        "date_created" : record.attrib.get("date-created", "").strip(),
        "summary" : summary_text,
        "has_summary": bool(summary_text),
        "alternative_names": alternative_names,
        "has_alt_name" : bool(alternative_names),
        "related_topics" : relative_topics,
        "has_rel_topics" : bool(relative_topics)
    }
    
    medical_data.append(data)

print("\n Medical data extraction and cleaning completed")
print("\n length of medical records : ", len(medical_data))


# Count records with empty summaries, title, description, not alternative, has relative topics? 
empty_summaries = sum(
    1 for data in medical_data
    if not data["has_summary"]
)

empty_titles = sum(
    1 for data in medical_data
    if not data["title"]
)

empty_descriptions = sum(
    1 for data in medical_data
    if not data["description"]
)

not_alt= sum(
    1 for data in medical_data
    if not data["has_alt_name"]
)

has_rel = sum(
    1 for data in medical_data
    if data["has_rel_topics"]
)


print("Records with empty summaries:", empty_summaries)
print("Records with empty titles:", empty_titles)
print("Records with empty descriptions:", empty_descriptions)
print("Records with no alternative names : ", not_alt) 
print("records with related topics (groups) : ", has_rel)


# Identify records with empty summaries, titles and description
for data in medical_data:
    
    if not data["has_summary"] or not data["description"] or not data["title"]:
        if not data["has_summary"]:
            print("\nNo Summary")
        else:
            print("\nHas Summary")
        if not data["description"]:
            print("No descrption")
        else:
            print("Has descreption")
        print("Title:", data["title"])
        print("ID:", data["id"])
        print("URL:", data["url"])
        
#Save records as Json file
output_path =  BASE_DIR / "data" / "processed" / "medical_data.json"
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as file:
    json.dump(medical_data, file, indent=4, ensure_ascii= False)
print("Json File saved : ", output_path)

