import os
from app.requirement_handling.file_handler import extract_text
from app.requirement_handling.topic_detection import detect_topics
from app.requirement_handling.topic_summary import summarize_topic
from app.requirement_handling.requirement_extractor import extract_requirements

# Global storage dict for all features
REQUIREMENTS_DICT = {}

def process_document(file_path):
    # Read file bytes
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    # Extract text from PDF
    filename = os.path.basename(file_path)
    text = extract_text(file_bytes, filename)

    # Step 1: Detect topics/features
    topics = detect_topics(text)
    if not topics:
        print("No topics detected.")
        return

    print("\nDetected Topics:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")

    id = 0

    # Step 2: Summarize topic + extract all requirements in ONE call per topic
    for topic in topics:
        
        print(f"\nProcessing topic: {topic}")
        summary = summarize_topic(text, topic)
        requirements = extract_requirements(text, topic)

        # Save to global dict
        REQUIREMENTS_DICT[id] = {
            "feature": topic, 
            "summary": summary,
            "requirements": requirements
        }
        id += 1
        


    print("\n=== REQUIREMENTS OUTPUT ===")
    for topic, data in REQUIREMENTS_DICT.items():
        print(f"\nFeature: {topic}")
        print(f"Summary: {data['summary']}")
        print(f"Requirements: {data['requirements']}")

    print(REQUIREMENTS_DICT)

if __name__ == "__main__":
    FILE_PATH = "app/requirement_handling/vaatimukset.pdf"  # Replace with your PDF
    process_document(FILE_PATH)
