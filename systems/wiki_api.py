import requests

WIKIPEDIA_API_URL = "https://es.wikipedia.org/w/api.php"
WIKIPEDIA_REST_URL = "https://es.wikipedia.org/api/rest_v1/page/random/summary"

def get_random_article():
    print("Obteniendo artículo aleatorio de Wikipedia...")
    headers = {
        "User-Agent": "DiscordBot/1.0 (contacto@example.com)" 
    }

    try:
        r = requests.get(WIKIPEDIA_REST_URL, headers=headers)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        print(f"Error en la petición: {e}")
        return {
            "title": "Error",
            "description": "",
            "image": ""
        }

    print(f"Artículo obtenido: {data['title']}")
    return {
        "id": data["pageid"],
        "title": data["title"],
        "description": data.get("extract", "Sin descripción"),
        "image": data.get("thumbnail", {}).get("source"),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
        "category": data.get("description")
    }
    
def get_wikipedia_categories(title):
    """Obtiene las categorías de un artículo de Wikipedia"""
    headers = {
        "User-Agent": "DiscordBot/1.0 (contacto@example.com)" 
    }
    params = {
        "action": "query",
        "prop": "categories",
        "titles": title,
        "format": "json",
        "cllimit": "max"
    }
    r = requests.get(WIKIPEDIA_API_URL, headers=headers, params=params, timeout=5)
    r.raise_for_status()
    data = r.json()
    page = next(iter(data["query"]["pages"].values()))
    categories = [cat["title"].lower() for cat in page.get("categories", [])]
    return categories

# Test
if __name__ == "__main__":
    article = get_random_article()
    print(article)