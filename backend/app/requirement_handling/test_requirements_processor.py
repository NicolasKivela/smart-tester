from app.requirement_handling.service import RequirementsProcessor
from app.requirement_handling.storage import REQUIREMENTS
import json


fake_json_input = '{"url": "https://example.com", "credentials": {"username": "test", "password": "1234"}}'
fake_text = """
The system must support login and password reset.
The user can purchase tickets and view schedules.
"""

processor = RequirementsProcessor(fake_json_input, fake_text, req_file=None)
processor.run_pipeline()

print("\n=== REQUIREMENTS OUTPUT ===")
for topic, data in REQUIREMENTS.items():
    print(f"\nFeature: {topic}")
    print(f"Summary: {data['summary']}")
    print(f"Requirements: {data['requirements']}")


# === Structured JSON view ===
print("\n=== RAW STORAGE DUMP (JSON Pretty Print) ===")
print(json.dumps(REQUIREMENTS, indent=2, ensure_ascii=False))