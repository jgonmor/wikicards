import requests

WIKIPEDIA_API_URL = "https://es.wikipedia.org/api/rest_v1/page/summary/"
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

def get_article_by_title(title: str) -> dict | None:
    headers = {"User-Agent": "DiscordBot/1.0 (contacto@example.com)"}
    url = WIKIPEDIA_API_URL + title
    try:
        r = requests.get(
            url,
            headers=headers,
            timeout=5
        )
        if r.status_code == 404:
            print(f"no se ha encontrado {url}")
            return None
        r.raise_for_status()
        data = r.json()
        return {
            "id": data["pageid"],
            "title": data["title"],
            "description": data.get("extract", "Sin descripción"),
            "image": data.get("thumbnail", {}).get("source"),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
            "category": data.get("description")
        }
    except requests.RequestException:
        print(f"error en la peticion a {url}")
        return None

# Test
if __name__ == "__main__":
    article = get_random_article()
    print(article)