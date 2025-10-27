LOCATORS = {
  "locators": 
    {
      "description": "Accept all cookies button",
      "css": "button.hslfi-cb__button-primary:text(\"Hyväksy kaikki\")",
      "xpath": "//button[normalize-space()='Hyväksy kaikki']",
      "page_url": "https://www.hsl.fi",
      "task": "Requirement 3.1: Browsing ticket types — As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },

    {
      "description": "Main navigation link for Tickets and Prices",
      "css": "a[data-testid='next-link'][href='/liput-ja-hinnat']:text(\"Liput ja hinnat\")",
      "xpath": "//a[text()='Liput ja hinnat' and @data-testid='next-link']",
      "page_url": "https://www.hsl.fi",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Button to buy a ticket, likely leading to ticket type selection",
      "css": "a.button.dark-blue:text(\"Osta lippu\")",
      "xpath": "//a[text()='Osta lippu']",
      "page_url": "https://www.hsl.fi",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Link to information about Ticket reform, potentially detailing new ticket types",
      "css": "a[data-testid='next-link'][href='/liput-ja-hinnat/lippu-uudistus']:text(\"Lippu-uudistus\")",
      "xpath": "//a[text()='Lippu-uudistus' and @data-testid='next-link']",
      "page_url": "https://www.hsl.fi",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Link to HSL app page, which may describe ticket types available via the app",
      "css": "a[data-testid='next-link'][href='/liput-ja-hinnat/hsl-sovellus']:text(\"HSL-sovellus\")",
      "xpath": "//a[text()='HSL-sovellus' and @data-testid='next-link']",
      "page_url": "https://www.hsl.fi",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Accept all cookies button",
      "css": "button:text('Hyväksy kaikki')",
      "xpath": "//button[text()='Hyväksy kaikki']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Main navigation link: Tickets and Prices (current page)",
      "css": "a[data-testid='next-link'][aria-current='page']:has-text('Liput ja hinnat')",
      "xpath": "//a[@data-testid='next-link' and @aria-current='page' and text()='Liput ja hinnat']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Main navigation link: Traveling",
      "css": "a[data-testid='next-link']:has-text('Matkustaminen')",
      "xpath": "//a[@data-testid='next-link' and text()='Matkustaminen']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Main navigation link: Customer Service",
      "css": "a[data-testid='next-link']:has-text('Asiakaspalvelu')",
      "xpath": "//a[@data-testid='next-link' and text()='Asiakaspalvelu']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Main navigation link: HSL (About HSL)",
      "css": "a[data-testid='next-link']:has-text('HSL')",
      "xpath": "//a[@data-testid='next-link' and text()='HSL']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link: Single Tickets",
      "css": "a[data-testid='next-link'][href*='/kertaliput']",
      "xpath": "//a[@data-testid='next-link' and contains(@href, '/kertaliput') and contains(normalize-space(), 'Kertaliput')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link: Serial Tickets",
      "css": "a[data-testid='next-link'][href*='/sarjaliput']",
      "xpath": "//a[@data-testid='next-link' and contains(@href, '/sarjaliput') and contains(normalize-space(), 'Sarjaliput')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link: Season Tickets",
      "css": "a[data-testid='next-link'][href*='/kausiliput']",
      "xpath": "//a[@data-testid='next-link' and contains(@href, '/kausiliput') and contains(normalize-space(), 'Kausiliput')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link: Continuous Subscriptions",
      "css": "a[data-testid='normal-link'][href*='/jatkuvan-tilauksen-liput']",
      "xpath": "//a[@data-testid='normal-link' and contains(@href, '/jatkuvan-tilauksen-liput') and contains(normalize-space(), 'Jatkuvat tilaukset')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link: Day Tickets",
      "css": "a[data-testid='next-link'][href*='/vuorokausiliput']",
      "xpath": "//a[@data-testid='next-link' and contains(@href, '/vuorokausiliput') and contains(normalize-space(), 'Vuorokausiliput')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link: Additional Zone Tickets",
      "css": "a[data-testid='next-link'][href*='#lisavyohykelippu']",
      "xpath": "//a[@data-testid='next-link' and contains(@href, '#lisavyohykelippu') and contains(normalize-space(), 'Lisävyöhykeliput')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Buy a ticket button",
      "css": "a.growth-button.dark-blue:has-text('Osta lippu')",
      "xpath": "//a[text()='Osta lippu' and contains(@class, 'growth-button')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Customer group selection dropdown toggle (e.g., Aikuinen)",
      "css": "button#customergroup-button",
      "xpath": "//button[@id='customergroup-button']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Zone selection dropdown toggle (e.g., AB)",
      "css": "button#zone-button",
      "xpath": "//button[@id='zone-button']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Municipality selection dropdown toggle (e.g., Helsinki)",
      "css": "button#municipality-button",
      "xpath": "//button[@id='municipality-button']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Show prices button (after filter selection)",
      "css": "button.ticket-price-selector__search__button:has-text('Näytä hinnat')",
      "xpath": "//button[text()='Näytä hinnat' and contains(@class, 'ticket-price-selector__search__button')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Find suitable ticket helper button",
      "css": "a.ticket-selection-helper__cta:has-text('Löydä sopiva lippu')",
      "xpath": "//a[text()='Löydä sopiva lippu' and contains(@class, 'ticket-selection-helper__cta')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Discount groups information link",
      "css": "a[data-testid='next-link'][href*='/alennusryhmat']",
      "xpath": "//a[@data-testid='next-link' and contains(@href, '/alennusryhmat') and text()='Alennusryhmät']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Accordion button for 'Vuoden 2025 hinnasto'",
      "css": "button#vuoden-2025-hinnasto-button",
      "xpath": "//button[@id='vuoden-2025-hinnasto-button']",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Link to 2025 Sep Price List PDF",
      "css": "a[data-testid='normal-link'][href*='22092025_fi.pdf']",
      "xpath": "//a[@data-testid='normal-link' and contains(@href, '22092025_fi.pdf') and contains(@aria-label, '22.9.2025 alkaen')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Next step: Link to 2025 Jan Price List PDF",
      "css": "a[data-testid='normal-link'][href*='27012025_fi.pdf']",
      "xpath": "//a[@data-testid='normal-link' and contains(@href, '27012025_fi.pdf') and contains(@aria-label, '27.1.2025 alkaen')]",
      "page_url": "https://www.hsl.fi/liput-ja-hinnat",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Accept all cookies button",
      "css": "button:has-text(\"Hyväksy kaikki\")",
      "xpath": "//button[text()='Hyväksy kaikki']",
      "page_url": "https://www.hsl.fi/matkustaminen",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Main navigation link to Tickets and Prices",
      "css": "a[data-testid='next-link'][href='/liput-ja-hinnat']",
      "xpath": "//a[@data-testid='next-link' and text()='Liput ja hinnat']",
      "page_url": "https://www.hsl.fi/matkustaminen",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Link to detailed Ticket Prices information",
      "css": "a[aria-label='Lippujen hinnat']",
      "xpath": "//a[text()='Lippujen hinnat' and @aria-label='Lippujen hinnat']",
      "page_url": "https://www.hsl.fi/matkustaminen",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Link for Adult Single Tickets with contactless payment",
      "css": "a[aria-label='Aikuisten kertaliput lähimaksulla']",
      "xpath": "//a[text()='Aikuisten kertaliput lähimaksulla']",
      "page_url": "https://www.hsl.fi/matkustaminen",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Link to information about tickets in the HSL app",
      "css": "a[aria-label='Liput HSL-sovelluksessa']",
      "xpath": "//a[text()='Liput HSL-sovelluksessa']",
      "page_url": "https://www.hsl.fi/matkustaminen",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Link to information about tickets on HSL card",
      "css": "a[aria-label='Liput HSL-kortilla']",
      "xpath": "//a[text()='Liput HSL-kortilla']",
      "page_url": "https://www.hsl.fi/matkustaminen",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Button to buy a ticket (may lead to ticket types selection)",
      "css": "a.button.growth-button.dark-blue:has-text(\"Osta lippu\")",
      "xpath": "//a[text()='Osta lippu' and contains(@class, 'button')]",
      "page_url": "https://www.hsl.fi/matkustaminen",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link for Tourists (likely contains specific ticket types like day tickets)",
      "css": "a[data-testid='next-link'][href='/matkustaminen/matkailijat']",
      "xpath": "//a[text()='Matkailijat' and @data-testid='next-link']",
      "page_url": "https://www.hsl.fi/matkustaminen",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Accept all cookies button to proceed",
      "css": "button.hslfi-cb__button-primary:has-text('Hyväksy kaikki')",
      "xpath": "//button[text()='Hyväksy kaikki']",
      "page_url": "https://www.hsl.fi/asiakaspalvelu",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Main navigation link to 'Tickets and prices' section",
      "css": "a[href='/liput-ja-hinnat']:has-text('Liput ja hinnat')",
      "xpath": "//a[@data-testid='next-link' and text()='Liput ja hinnat']",
      "page_url": "https://www.hsl.fi/asiakaspalvelu",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link for 'Tips for buying a ticket'",
      "css": "a[href='/asiakaspalvelu/tuki-ja-ohjeet/lippuohjeet']:has-text('Vinkit lipun ostoon')",
      "xpath": "//a[text()='Vinkit lipun ostoon']",
      "page_url": "https://www.hsl.fi/asiakaspalvelu",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link for 'How to buy a ticket for a child'",
      "css": "a[href='/liput-ja-hinnat/alennusryhmat/lapset']:has-text('Miten ostan lipun lapselle?')",
      "xpath": "//a[text()='Miten ostan lipun lapselle?']",
      "page_url": "https://www.hsl.fi/asiakaspalvelu",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link for 'Help with using HSL app' (may cover ticket types via app)",
      "css": "a[href='/liput-ja-hinnat/hsl-sovellus']:has-text('Apua HSL-sovelluksen käyttöön')",
      "xpath": "//a[text()='Apua HSL-sovelluksen käyttöön']",
      "page_url": "https://www.hsl.fi/asiakaspalvelu",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Category link to 'Support and instructions' page (parent of ticket-related info)",
      "css": "a[href='/asiakaspalvelu/tuki-ja-ohjeet']:has-text('Tuki ja ohjeet')",
      "xpath": "//a[text()='Tuki ja ohjeet' and contains(@class, 'Button_buttonLink')]",
      "page_url": "https://www.hsl.fi/asiakaspalvelu",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Accept all cookies button",
      "css": "button.hslfi-cb__button-primary:has-text('Hyväksy kaikki')",
      "xpath": "//button[text()='Hyväksy kaikki' and contains(@class, 'hslfi-cb__button-primary')]",
      "page_url": "https://www.hsl.fi/hsl",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Main menu link to Tickets and Prices (leading to ticket types information)",
      "css": "a[href='/liput-ja-hinnat'][data-testid='next-link']:has-text('Liput ja hinnat')",
      "xpath": "//a[@href='/liput-ja-hinnat' and text()='Liput ja hinnat']",
      "page_url": "https://www.hsl.fi/hsl",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Main call-to-action button to buy a ticket (initiates purchase flow, likely after selecting ticket type)",
      "css": "a.growth-button:has-text('Osta lippu')",
      "xpath": "//a[text()='Osta lippu' and contains(@class, 'growth-button')]",
      "page_url": "https://www.hsl.fi/hsl",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    },
    {
      "description": "Link to HSL application page (for buying tickets via app, likely detailing ticket types)",
      "css": "a[href='/liput-ja-hinnat/hsl-sovellus']:has-text('HSL-sovellus')",
      "xpath": "//a[@href='/liput-ja-hinnat/hsl-sovellus' and text()='HSL-sovellus']",
      "page_url": "https://www.hsl.fi/hsl",
      "task": "Requirement 3.1: Browsing ticket types As a user, I want to find information about different ticket types (e.g., single, day, and season tickets), so that I can choose the most suitable ticket for my needs."
    }
  ]
}