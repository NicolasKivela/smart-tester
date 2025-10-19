import asyncio
from playwright.async_api import async_playwright
from locator_agent import LocatorRetrievalAgent

async def handle_cookies(page):
    """Yritetään hyväksyä tai poistaa cookie-banneri."""
    selectors = [
        ".coi-banner__accept",
        "button[aria-label='OK']",
        "#onetrust-accept-btn-handler",
        "#accept-cookies",
        "#cookie-accept",
        "button:has-text('Hyväksy')",
        "button:has-text('OK')",
        "button:has-text('Accept')",
        "text='Hyväksy kaikki'",
        "#coiOverlay"
    ]
    
    for sel in selectors:
        try:
            locator = page.locator(sel)
            if await locator.count() > 0:
                await locator.first.click(timeout=3000)
                await asyncio.sleep(1)
                print(f"🍪 Cookie-banneri hyväksytty/poistettu: {sel}")
                return
        except Exception:
            pass

    # Jos hyväksyntäpainiketta ei löydy, poistetaan overlay manuaalisesti
    try:
        await page.evaluate("""() => {
            const overlay = document.querySelector('#coiOverlay');
            const wrapper = document.querySelector('#cookie-information-template-wrapper');
            if (overlay) overlay.remove();
            if (wrapper) wrapper.remove();
        }""")
        print("🍪 Cookie-overlay poistettu manuaalisesti.")
    except Exception:
        pass


async def navigate_site(start_url: str, task: str, max_depth=2):
    agent = LocatorRetrievalAgent()
    visited = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        async def process_page(url, depth):
            if url in visited or depth > max_depth:
                return
            visited.add(url)

            print(f"\n🌐 [Depth {depth}] Käsitellään: {url}")
            await page.goto(url, timeout=60000)
            await asyncio.sleep(2)
            await handle_cookies(page)

            locators = agent.execute(url, task)
            if not locators:
                print("⚠️ Ei relevantteja lokaattoreita tälle sivulle.")
                return

            for loc in locators:
                desc = loc.get("description")
                css = loc.get("css")
                xpath = loc.get("xpath")
                locator = css if css and css != "N/A" else xpath

                if not locator or locator == "N/A":
                    continue

                print(f"➡️ Klikataan: {desc}")
                try:
                    el = page.locator(locator)
                    if await el.count() == 0:
                        print(f"❌ Elementtiä ei löytynyt: {locator}")
                        continue

                    await el.first.click(timeout=5000)
                    await asyncio.sleep(3)

                    new_url = page.url
                    if new_url != url and new_url not in visited:
                        print(f"🔗 Uusi sivu: {new_url}")
                        await process_page(new_url, depth + 1)
                        # palataan alkuun
                        await page.goto(url)
                        await handle_cookies(page)
                        await asyncio.sleep(2)

                except Exception as e:
                    print(f"⚠️ Klikkaus epäonnistui: {e}")

        # aloitetaan navigointi
        await process_page(start_url, 1)

        print("✅ Navigointi valmis. Kaikki lokaattorit tallennettu locators.json-tiedostoon.")
        await browser.close()
