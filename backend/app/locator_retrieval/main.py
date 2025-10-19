import asyncio
from navigator import navigate_site

def main():
    start_url = "https://www.gigantti.fi"
    task = "Find locators relevant for navigating into the gamingmouses gategory without using search bar"
    depth = int(input("Kuinka syvälle mennään (esim. 2): "))
    asyncio.run(navigate_site(start_url, task, max_depth=depth))

if __name__ == "__main__":
    main()
