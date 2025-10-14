import os
from app.requirement_handling.file_handler import extract_text
from app.requirement_handling.topic_detection import detect_topics
from app.requirement_handling.topic_summary import summarize_topic
from app.requirement_handling.requirement_extractor import extract_requirements
from app.requirement_handling.save_file import save_to_file

OUTPUT_DIR = "app/requirement_handling/output"


def process_document(file_path):
    # Extract text
    text = extract_text(file_path)

    # PASS 1: Detect Topics
    topics = detect_topics(text)
    if not topics:
        print("No topics detected.")
        return

    print("\nDetected Topics:")
    for i, t in enumerate(topics, 1):
        print(f"  {i}. {t}")

    # PASS 2: Summarize Each Topic
    summaries = {}
    for topic in topics:
        summary = summarize_topic(text, topic)
        summaries[topic] = summary
        save_to_file(OUTPUT_DIR, f"{topic}_summary.txt", summary)

    print("\nSummaries saved in 'output/' folder.")

    # User selects topics for detailed extraction
    selected = input("Enter topic numbers for detailed requirement extraction (comma or 'all'): ")
    if selected.lower().strip() == "all":
        selected_topics = topics
    else:
        selected_topics = [topics[int(i.strip()) - 1] for i in selected.split(",")]

    # PASS 3: Extract Requirements
    for topic in selected_topics:
        requirements = extract_requirements(text, topic)
        save_to_file(OUTPUT_DIR, f"{topic}_requirements.json", requirements)
        print(f"{topic} requirements saved.")

    print("\nAll processing done! Check 'output/' folder for results.")



if __name__ == "__main__":
    FILE_PATH = "app/requirement_handling/vaatimukset.pdf"  # Replace with your PDF file path

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    process_document(FILE_PATH)
    """
    text = extract_text(FILE_PATH)
    print("Extracting text...")
    print("===== Extracted Text =====")
    print(text)
    """


