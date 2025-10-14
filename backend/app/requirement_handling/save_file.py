import os

def save_to_file(folder, filename, content):
    """Save text content to file in the given folder."""

    try:
        os.makedirs(folder, exist_ok=True)

        path = os.path.join(folder, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None