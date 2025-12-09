import os
import json


def save_to_file(output_dir, filename, content):
    """Save string or JSON-serializable content to a file."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            # If it's a list or dict, convert to pretty JSON
            if isinstance(content, (list, dict)):
                f.write(json.dumps(content, indent=2, ensure_ascii=False))
            else:
                f.write(str(content))
    except Exception as e:
        print(f"An error occurred: {e}")

        