import asyncio
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

class PageNavigator:
    """
    A class to encapsulate Playwright browser interactions.
    """
    def __init__(self, headless: bool = False):
        self.playwright = None
        self.browser = None
        self.page = None
        self.headless = headless

    async def start(self):
        """Starts the Playwright instance and launches a browser."""
        print("Starting browser...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = await context.new_page()
        print("Browser started.")

    async def stop(self):
        """Stops the browser and the Playwright instance."""
        print("Stopping browser...")
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser stopped.")

    async def navigate(self, url: str) -> str:
        """Navigates the page to a specified URL."""
        print(f"Navigating to {url}...")
        try:
            await self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
            await self._handle_cookies()
            return f"Successfully navigated to {url}. Current URL is {self.page.url}."
        except Exception as e:
            return f"Failed to navigate to {url}. Error: {e}"

    async def click(self, selector: str, description: str) -> str:
        """Clicks an element on the page matching the given CSS selector."""
        print(f"Attempting to click: {description} (Selector: {selector})")
        try:
            await self.page.locator(selector).first.click(timeout=10000)
            await self.page.wait_for_load_state('domcontentloaded', timeout=10000)
            return f"Clicked element '{description}' with selector '{selector}'. Current URL is {self.page.url}."
        except Exception as e:
            return f"Failed to click element with selector '{selector}'. Error: {e}"

    async def fill(self, selector: str, text: str, description: str) -> str:
        """Fills an input field with the given text."""
        print(f"Attempting to fill: {description} (Selector: {selector})")
        try:
            await self.page.locator(selector).first.fill(text, timeout=5000)
            return f"Filled input '{description}' with selector '{selector}'."
        except Exception as e:
            return f"Failed to fill element with selector '{selector}'. Error: {e}"

    async def get_page_content(self) -> str:
        """
        Returns a string containing the current URL and a simplified view of the
        interactive elements on the page (links, buttons, inputs).
        """
        try:
            await self.page.wait_for_load_state('domcontentloaded', timeout=10000)
            content = f"Current URL: {self.page.url}\n\n"
            
            html = await self.page.content()
            soup = BeautifulSoup(html, 'html.parser')

            elements = []
            for el in soup.find_all(['a', 'button', 'input', 'textarea', 'select']):
                text = ' '.join(el.stripped_strings)
                # Create a CSS selector for the element
                selector = el.name
                if el.has_attr('id'):
                    selector = f"#{el['id']}"
                elif el.has_attr('data-testid'):
                    selector = f"[{el.name}[data-testid='{el['data-testid']}']"
                elif text:
                    # This is a simplification, but can work for many cases
                    selector = f"{el.name}:has-text('{text}')"

                element_info = f"- Element: <{el.name}>, Text: '{text}', Selector suggestion: '{selector}'"
                elements.append(element_info)
            
            content += "Interactive elements on page:\n"
            if elements:
                content += "\n".join(elements)
            else:
                content += "No interactive elements found."
                
            return content
        except Exception as e:
            return f"Failed to get page content. Error: {e}"

    async def _handle_cookies(self):
        """Attempts to accept or dismiss cookie banners."""
        selectors = [
            "button:has-text('Accept all')",
            "button:has-text('Accept')",
            "button:has-text('Hyväksy kaikki')",
            "button:has-text('Hyväksy')",
            "#onetrust-accept-btn-handler",
        ]
        for selector in selectors:
            try:
                locator = self.page.locator(selector)
                if await locator.count() > 0:
                    await locator.first.click(timeout=1000)
                    print(f"Cookie banner handled with selector: {selector}")
                    await self.page.wait_for_load_state('domcontentloaded', timeout=5000)
                    return
            except Exception:
                continue
        print("No cookie banner found or it was not clickable.")
