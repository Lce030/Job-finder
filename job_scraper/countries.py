"""Countries supported by the Adzuna API, with their code and currency."""

# https://developer.adzuna.com/overview -> available countries
ADZUNA_COUNTRIES = {
    "Australia": "au",
    "Austria": "at",
    "Belgium": "be",
    "Brazil": "br",
    "Canada": "ca",
    "France": "fr",
    "Germany": "de",
    "India": "in",
    "Italy": "it",
    "Mexico": "mx",
    "Netherlands": "nl",
    "New Zealand": "nz",
    "Poland": "pl",
    "Singapore": "sg",
    "South Africa": "za",
    "Spain": "es",
    "Switzerland": "ch",
    "United Kingdom": "gb",
    "United States": "us",
}

CURRENCY_BY_COUNTRY = {
    "at": "EUR", "au": "AUD", "be": "EUR", "br": "BRL", "ca": "CAD",
    "ch": "CHF", "de": "EUR", "es": "EUR", "fr": "EUR", "gb": "GBP",
    "in": "INR", "it": "EUR", "mx": "MXN", "nl": "EUR", "nz": "NZD",
    "pl": "PLN", "sg": "SGD", "us": "USD", "za": "ZAR",
}

# Special option: skips country filtering and uses remote/global job sources.
REMOTE_OPTION = "Remote / Global"

# Alternative names used to filter by location in sources that don't support
# country filtering directly (Arbeitnow, RemoteOK), since their job postings
# describe the location in these languages.
LOCATION_HINTS = {
    "Australia": ["australia"],
    "Austria": ["austria", "österreich"],
    "Belgium": ["belgium", "belgique", "belgië"],
    "Brazil": ["brazil", "brasil"],
    "Canada": ["canada"],
    "France": ["france"],
    "Germany": ["germany", "deutschland"],
    "India": ["india"],
    "Italy": ["italy", "italia"],
    "Mexico": ["mexico", "méxico"],
    "Netherlands": ["netherlands", "holland"],
    "New Zealand": ["new zealand"],
    "Poland": ["poland", "polska"],
    "Singapore": ["singapore"],
    "South Africa": ["south africa"],
    "Spain": ["spain", "españa"],
    "Switzerland": ["switzerland", "schweiz", "suisse"],
    "United Kingdom": ["united kingdom", "england", "scotland", "wales"],
    "United States": ["united states", "usa", "u.s."],
}

# Major cities mapped to their country. Sources like Arbeitnow and RemoteOK
# often give a city name with no country, so this lets us still match a job
# to the requested country.
CITY_HINTS = {
    "sydney": "Australia", "melbourne": "Australia", "brisbane": "Australia", "perth": "Australia",
    "vienna": "Austria", "wien": "Austria", "graz": "Austria", "salzburg": "Austria", "linz": "Austria",
    "brussels": "Belgium", "antwerp": "Belgium", "ghent": "Belgium", "leuven": "Belgium",
    "sao paulo": "Brazil", "são paulo": "Brazil", "rio de janeiro": "Brazil", "belo horizonte": "Brazil",
    "toronto": "Canada", "vancouver": "Canada", "montreal": "Canada", "ottawa": "Canada", "calgary": "Canada",
    "paris": "France", "lyon": "France", "marseille": "France", "toulouse": "France", "nantes": "France", "bordeaux": "France", "lille": "France",
    "berlin": "Germany", "munich": "Germany", "münchen": "Germany", "hamburg": "Germany", "frankfurt": "Germany",
    "cologne": "Germany", "köln": "Germany", "stuttgart": "Germany", "düsseldorf": "Germany", "dusseldorf": "Germany",
    "dresden": "Germany", "leipzig": "Germany", "nuremberg": "Germany", "nürnberg": "Germany", "bremen": "Germany",
    "hanover": "Germany", "hannover": "Germany", "essen": "Germany", "dortmund": "Germany", "bonn": "Germany", "aachen": "Germany",
    "bangalore": "India", "bengaluru": "India", "mumbai": "India", "delhi": "India", "hyderabad": "India", "pune": "India", "chennai": "India",
    "rome": "Italy", "roma": "Italy", "milan": "Italy", "milano": "Italy", "turin": "Italy", "torino": "Italy", "naples": "Italy",
    "mexico city": "Mexico", "ciudad de méxico": "Mexico", "guadalajara": "Mexico", "monterrey": "Mexico",
    "amsterdam": "Netherlands", "rotterdam": "Netherlands", "utrecht": "Netherlands", "the hague": "Netherlands", "eindhoven": "Netherlands",
    "auckland": "New Zealand", "wellington": "New Zealand", "christchurch": "New Zealand",
    "warsaw": "Poland", "warszawa": "Poland", "krakow": "Poland", "kraków": "Poland", "wroclaw": "Poland", "wrocław": "Poland", "poznan": "Poland",
    "johannesburg": "South Africa", "cape town": "South Africa", "pretoria": "South Africa", "durban": "South Africa",
    "madrid": "Spain", "barcelona": "Spain", "valencia": "Spain", "seville": "Spain", "sevilla": "Spain", "bilbao": "Spain", "malaga": "Spain", "málaga": "Spain", "zaragoza": "Spain",
    "zurich": "Switzerland", "zürich": "Switzerland", "geneva": "Switzerland", "basel": "Switzerland", "bern": "Switzerland", "lausanne": "Switzerland",
    "london": "United Kingdom", "manchester": "United Kingdom", "birmingham": "United Kingdom", "edinburgh": "United Kingdom",
    "glasgow": "United Kingdom", "leeds": "United Kingdom", "bristol": "United Kingdom", "cambridge": "United Kingdom", "oxford": "United Kingdom",
    "new york": "United States", "san francisco": "United States", "los angeles": "United States", "chicago": "United States",
    "austin": "United States", "seattle": "United States", "boston": "United States", "denver": "United States", "atlanta": "United States",
    "singapore": "Singapore",
}


def get_location_hints(country_name: str) -> list[str]:
    """Returns the country names and major city names used to match a given
    country against the free-text location fields of sources that don't
    support filtering by country directly (Arbeitnow, RemoteOK)."""
    hints = list(LOCATION_HINTS.get(country_name, []))
    hints += [city for city, country in CITY_HINTS.items() if country == country_name]
    return hints
