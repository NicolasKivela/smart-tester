import asyncio
import datetime
import os
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

class PageNavigator:
    """
    A class to encapsulate Playwright browser interactions.
    """
    def __init__(self, headless: bool = True, silent: bool = False, video_path: str | None = None):
        self.playwright = None
        self.browser = None
        self.context = None # Add context as an instance variable
        self.page: Page | None = None
        self.headless = headless
        self.silent = silent
        self.video_path = video_path

    async def start(self):
        """Starts the Playwright instance and launches a browser."""
        if not self.silent:
            print("Starting browser...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        
        context_options = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        if self.video_path:
            if not os.path.exists(self.video_path):
                os.makedirs(self.video_path)
            context_options['record_video_dir'] = self.video_path
            context_options['record_video_size'] = {'width': 1920, 'height': 1080} # Optional: specify video size

        self.context = await self.browser.new_context(**context_options)
        self.page = await self.context.new_page()
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
        cookie_locator = self.page.get_by_role("button", name="Hyväksy kaikki")
        
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

    async def execute_action(self, action_details: dict):
        """
        Parses and executes a single action (e.g., 'click') from an agent.
        """
        if not self.page:
            raise Exception("Page is not initialized.")

        action_type = action_details.get('action')

        if action_type == "click":
            selector = action_details.get('css') or action_details.get('xpath')
            if not selector:
                if not self.silent:
                    print("Action was 'click' but no selector was provided.")
                return

            try:
                if not self.silent:
                    print(f"Executing action: '{action_type}' by clicking selector: {selector}")
                await self.page.locator(selector).first.click(timeout=10000)
                if not self.silent:
                    print("Click successful.")
                await self.page.wait_for_load_state("networkidle", timeout=10000)
            except Exception as e:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"failure_{timestamp}.png"
                await self.page.screenshot(path=screenshot_path)
                if not self.silent:
                    print(f"Click action failed for selector '{selector}'. Screenshot saved to {screenshot_path}. Reason: {e}")
                raise e
        # Can add more actions like 'fill' here in the future
        elif action_type == "fill":
            selector = action_details.get('css') or action_details.get('xpath')
            text = action_details.get('possible text')

            if not selector or text == "N/A":
                if not self.silent:
                    print("Action was 'fill' but selector or value was missing.")
                return
            try:
                if not self.silent:
                    print(f"Executing action: '{action_type}' by filling selector: {selector} with value: '{text}'")
                await self.page.locator(selector).first.fill(text, timeout=10000)
                if not self.silent:
                    print(f"Filled '{selector}' successfully with '{text}'.")
            except Exception as e:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"failure_{timestamp}.png"
                await self.page.screenshot(path=screenshot_path)
                if not self.silent:
                    print(f"Fill action failed for selector '{selector}'. Screenshot saved to {screenshot_path}. Reason: {e}")
                raise e        



        else:
            if not self.silent:
                print(f"Action was '{action_type}', not 'click' or 'fill'. Skipping execution.")

    async def get_page_content_for_agent(self, task: str) -> str:
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

        selectors = ['input', 'button', 'a', 'select', 'textarea', 'label', 'submit', 'listbox',]
        elements = soup.find_all(selectors)
        
        interactive_elements = [str(el) for el in elements]
        locators_string = ", ".join(interactive_elements)
        
        return f"URL: {self.page.url}, Locators: {locators_string}, Task: {str(task)}"

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