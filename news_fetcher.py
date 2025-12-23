import requests

def fetch_news(api_key, country="in", category=None, city=None):
    """
    Fetch category-wise unique news for country + city fallback.
    """
    articles = []

    # Prepare query
    country_query = country
    if category:
        country_query += f" AND {category}"

    # 1️⃣ City-specific news
    if city:
        url_city = f"https://newsapi.org/v2/everything?q={city} AND {category or ''}&sortBy=publishedAt&language=en&apiKey={api_key}"
        response = requests.get(url_city).json()
        articles.extend(response.get("articles", []))

    # 2️⃣ Country-specific news
    url_country = f"https://newsapi.org/v2/everything?q={country_query}&sortBy=publishedAt&language=en&apiKey={api_key}"
    response = requests.get(url_country).json()
    articles.extend(response.get("articles", []))

    # Deduplicate by title
    seen = set()
    unique_articles = []
    for a in articles:
        if a["title"] not in seen:
            unique_articles.append(a)
            seen.add(a["title"])

    return unique_articles
