
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_interactive_elements(url: str) -> list[str]:
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9',
        })

        await page.goto(url, timeout=60000, wait_until="networkidle")

        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, 'html.parser')

    selectors = ['input', 'button', 'a', 'select', 'textarea', 'label', 'submit']
    elements = soup.find_all(selectors)

    # Palautetaan elementtien ulompi HTML-rakenne
    return [str(el) for el in elements]


