import asyncio
import datetime
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

class PageNavigator:
    """
    A class to encapsulate Playwright browser interactions.
    """
    def __init__(self, headless: bool = True, silent: bool = False):
        self.playwright = None
        self.browser = None
        self.page: Page | None = None
        self.headless = headless
        self.silent = silent

    async def start(self, record_video_dir: str = None):
        """Starts the Playwright instance and launches a browser."""
        if not self.silent:
            print("Starting browser...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        
        context_args = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        if record_video_dir:
            context_args['record_video_dir'] = record_video_dir
            if not self.silent:
                print(f"Recording video to {record_video_dir}")

        context = await self.browser.new_context(**context_args)
        self.page = await context.new_page()
        if not self.silent:
            print("Browser started.")

    async def goto(self, url: str):
        """Navigates the page to a specified URL."""
        if not self.page:
            raise Exception("Page is not initialized. Call start() first.")
        if not self.silent:
            print(f"Navigating to {url}...")
        await self.page.goto(url, timeout=60000, wait_until="networkidle")

    async def accept_cookies(self):
        """Finds and clicks the cookie acceptance button."""
        if not self.page:
            raise Exception("Page is not initialized.")
            
        # As requested, a placeholder for the locator.
        cookie_locator = self.page.get_by_role("button", name="Accept all")
        
        if not self.silent:
            print("Checking for and clicking cookie consent button...")
        await self.page.wait_for_timeout(2000)
        try:
            await cookie_locator.click(timeout=5000)
            if not self.silent:
                print("Cookie consent button clicked.")
            await self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception as e:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"failure_{timestamp}.png"
                await self.page.screenshot(path=screenshot_path)
                if not self.silent:
                    print(f"Click action failed for selector in cookie consent'{cookie_locator}'. Screenshot saved to {screenshot_path}. Reason: {e}")

    async def iteration_screenshot(self, iteration: int):
        """Takes a screenshot of the page, in the current iteration"""
        if not self.page:
            raise Exception("Page is not initialized.")
        screenshot_path = f"iteration_{iteration}.png"
        await self.page.screenshot(path=screenshot_path)
        if not self.silent:
            print(f"Screenshot saved to {screenshot_path}")                

    async def execute_action(self, action_details: dict):
        """
        Parses and executes a single action (e.g., 'click') from an agent.
        """
        if not self.page:
            raise Exception("Page is not initialized.")

        action_type = action_details.get('action')

        try:
            if action_type == "click":
                selector = action_details.get('css') or action_details.get('xpath')
                if not selector:
                    if not self.silent:
                        print("Action was 'click' but no selector was provided.")
                    return

                if not self.silent:
                    print(f"Executing action: '{action_type}' by clicking selector: {selector}")
                await self.page.locator(selector).first.click(timeout=10000)
                if not self.silent:
                    print("Click successful.")
                await self.page.wait_for_load_state("networkidle", timeout=10000)

            elif action_type == "fill":
                selector = action_details.get('css') or action_details.get('xpath')
                text_value = action_details.get('possible text') or "tickets and prices" # Fallback or specific field

                if not selector:
                    if not self.silent:
                        print("Action was 'fill' but selector was missing.")
                    return
                
                if not self.silent:
                    print(f"Executing action: '{action_type}' by filling selector: {selector} with value: '{text_value}'")
                await self.page.locator(selector).first.fill(text_value, timeout=10000)
                if not self.silent:
                    print(f"Filled '{selector}' successfully.")

            elif action_type == "press_enter":
                selector = action_details.get('css') or action_details.get('xpath')
                if not selector:
                    if not self.silent:
                        print("Action was 'press_enter' but no selector was provided.")
                    return

                if not self.silent:
                    print(f"Executing action: '{action_type}' on selector: {selector}")
                await self.page.locator(selector).first.press("Enter", timeout=10000)
                if not self.silent:
                    print("Press Enter successful.")
                await self.page.wait_for_load_state("networkidle", timeout=10000)

            elif action_type == "goto":
                url = action_details.get('url')
                if not url:
                    if not self.silent:
                        print("Action was 'goto' but no URL was provided.")
                    return

                if not self.silent:
                    print(f"Executing action: '{action_type}' to URL: {url}")
                await self.page.goto(url, timeout=60000, wait_until="networkidle")
                if not self.silent:
                    print(f"Navigated to {url} successfully.")

            else:
                if not self.silent:
                    print(f"Action was '{action_type}', skipping execution.")

        except Exception as e:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"failure_{timestamp}.png"
            await self.page.screenshot(path=screenshot_path)
            if not self.silent:
                print(f"Action '{action_type}' failed. Screenshot saved to {screenshot_path}. Reason: {e}")
            raise e

    async def get_page_content_for_agent(self, scenarios: str) -> str:
        """
        Scrapes the page and formats the content as a prompt for the LocatorRetrievalAgent.
        """
        if not self.page:
            raise Exception("Page is not initialized.")

        if not self.silent:
            print("Scraping current page for interactive elements...")
        try:
            await self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            if not self.silent:
                print(f"Page did not reach network idle state, continuing anyway. Reason: {e}")

        html = await self.page.content()
        soup = BeautifulSoup(html, 'html.parser')

        selectors = ['input', 'button', 'a', 'select', 'textarea', 'label', 'submit']
        elements = soup.find_all(selectors)
        
        interactive_elements = []
        for el in elements:
            # Extract only essential attributes
            attrs = {
                'tag': el.name,
                'text': el.get_text(strip=True)[:50], # Limit text length
                'id': el.get('id'),
                'class': el.get('class'),
                'name': el.get('name'),
                'type': el.get('type'),
                'role': el.get('role'),
                'href': el.get('href'),
                'placeholder': el.get('placeholder'),
                'aria-label': el.get('aria-label'),
                'title': el.get('title')
            }
            # Remove None values
            clean_attrs = {k: v for k, v in attrs.items() if v}
            interactive_elements.append(str(clean_attrs))

        locators_string = ", ".join(interactive_elements)
        
        return f"URL: {self.page.url}, Locators: {locators_string}, Scenarios: {str(scenarios)}"

    async def get_aria_snapshot(self) -> str:
        """
        Captures the aria snapshot of the current page.
        """
        if not self.page:
            raise Exception("Page is not initialized.")
        try:
            # Playwright's aria_snapshot is available on the locator or page.
            # Using page.locator("body") to get the whole page snapshot or just page.accessibility.snapshot()
            # Wait, aria_snapshot is a specific method in newer playwright versions.
            # Let's try to use the locator('body').aria_snapshot() if available, or fallback.
            # Actually, the user asked for "playwright's aria-snapshot". 
            # It is likely `await page.locator("body").aria_snapshot()`
            snapshot = await self.page.locator("body").aria_snapshot()
            return snapshot
        except Exception as e:
            if not self.silent:
                print(f"Failed to get aria snapshot: {e}")
            return ""

    async def get_screenshot(self) -> str:
        """
        Captures a screenshot and returns it as a base64 encoded string.
        """
        if not self.page:
            raise Exception("Page is not initialized.")
        try:
            import base64
            screenshot_bytes = await self.page.screenshot(type='jpeg', quality=50)
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            return screenshot_b64
        except Exception as e:
            if not self.silent:
                print(f"Failed to get screenshot: {e}")
            return ""

    async def stop(self):
        """Stops the browser and the Playwright instance."""
        if not self.silent:
            print("Stopping browser...")
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        if not self.silent:
            print("Browser stopped.")