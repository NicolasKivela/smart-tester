import os
import json
import re
from google import genai
from dotenv import load_dotenv
from scraper import scrape_interactive_elements

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY puuttuu .env tiedostosta")

client = genai.Client(api_key=api_key)

class LocatorRetrievalAgent:
    def __init__(self, model="gemini-2.5-flash", output_file="locators.json"):
        self.model = model
        self.output_file = output_file
        # luodaan tiedosto jos ei ole
        if not os.path.exists(self.output_file):
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump({"locators": []}, f, indent=2, ensure_ascii=False)

    async def execute(self, url: str, task: str) -> list:
        scraped_elements = await scrape_interactive_elements(url)
        print(f"🧠 Analysoidaan {url} tehtävällä: {task}")

        # Muotoillaan kaavittu data selkeämmin kehotteeseen
        html_snippets = "\n".join(scraped_elements)

        prompt = f"""
        You are a senior Test Automation Engineer using Playwright.

        Your task is: "{task}" on page: {url}

        I have scraped all interactive elements and here is the raw HTML for them.
        Please identify **all potentially useful locators** for this task, including:
        - main menu buttons
        - category links
        - product links
        - add-to-cart buttons
        - next navigation steps

        Return only valid JSON in this format:
        {{
        "locators": [
            {{
            "description": "<short readable name>",
            "css": "<CSS selector or N/A>",
            "xpath": "<XPath selector or N/A>"
            }}
        ]
        }}

        Here are all scraped elements:
        {html_snippets}
        """

        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        raw = response.text.strip()
        match = re.search(r"\{[\s\S]*\}", raw)
        json_text = match.group(0) if match else raw

        try:
            data = json.loads(json_text)
        except Exception:
            print("⚠️ JSON parsing failed. Using fallback empty data.")
            data = {"locators": []}

        # Lisää url jokaiseen lokaattoriin
        for loc in data.get("locators", []):
            loc["page_url"] = url
            loc["task"] = task

        # Tallenna yhteen tiedostoon
        self.save_locators(data.get("locators", []))
        return data.get("locators", [])

    def save_locators(self, new_locators: list):
        try:
            with open(self.output_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = {"locators": []}

        existing["locators"].extend(new_locators)

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        print(f"💾 {len(new_locators)} lokaattoria lisätty tiedostoon {self.output_file}")
