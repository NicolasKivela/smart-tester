import requests
from bs4 import BeautifulSoup, Tag

def scrape_interactive_elements(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    selectors = ['input', 'button', 'a', 'select', 'textarea', 'label', 'submit']
    elements = soup.find_all(selectors)

    simplified = []
    for i, el in enumerate(elements):
        if not isinstance(el, Tag):
            continue
        attrs = {k: v for k, v in el.attrs.items() if v}
        text = el.get_text(strip=True)
        if len(text) > 80:
            text = text[:77] + "..."
        simplified.append(f"[{i+1}] <{el.name}> text='{text}' attrs={attrs}")

    return "\n".join(simplified)


