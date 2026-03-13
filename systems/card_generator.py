import random
from .wiki_api import get_random_article, get_article_by_title
from database.models.card_model import CardModel
from .ai_classifier import DeepseekClassifier

_classifier = DeepseekClassifier()

TIPOS_ES = {
    "Científico": ["científico", "físico", "químico", "biólogo", "matemático", "ingeniero", "astrónomo"],
    "Actor": ["actor", "actriz", "cine", "película", "teatro", "serie"],
    "Músico": ["músico", "cantante", "banda", "compositor", "álbum", "canción"],
    "Deportista": ["futbolista", "jugador", "deporte", "atleta", "tenista", "baloncesto"],
    "Político": ["político", "presidente", "gobierno", "ministro", "diputado", "senador"],
    "Escritor": ["escritor", "poeta", "novela", "literatura", "autor", "cuento"],
    "Lugar": ["ciudad", "país", "provincia", "municipio", "localidad", "región"],
    "Animal": ["animal", "mamífero", "ave", "pez", "reptil", "insecto"],
    "Obra": ["película", "libro", "novela", "canción", "álbum", "serie"],
    "Invento": ["inventor", "invento", "tecnología", "dispositivo", "máquina"],
    "Evento": ["guerra", "batalla", "acontecimiento", "historia", "revolución"],
    "Arquitectura": ["casa", "edificio", "construccion", "arquitectura"],
    "General": []  # Para artículos que no encajen en los anteriores
}

MITICOS = ["shrek", "cristiano ronaldo", "osama bin laden", "pedro sanchez", "mariano rajoy", "francisco franco", "adolf hitler"]

def rarity(title):
    print(f'Generando rareza de la carta...')
    text = f"{title}".lower()
    if text in MITICOS:
        return "Mítico"
    
    roll = random.randint(1, 100)
    
    if roll <= 60:
        return "Común"
    elif roll <= 85:
        return "Raro"
    elif roll <= 95:
        return "Épico"
    elif roll <= 99:
        return "Legendario"
    else:
        return "Mítico"
    
def generate_stats(rarity):
   
   print(f'Generando estadísticas para rareza: {rarity}...') 
    
   ranges = {
        "Común": (30, 50),
        "Raro": (50, 70),
        "Épico": (70, 90),
        "Legendario": (90, 110),
        "Mítico": (110, 130)
    }
   
   low, high = ranges[rarity]
   
   print(f'rango de stats {low} {high}')
   
   return {
        'attack': random.randint(low, high),
        'defense': random.randint(low, high),
        'hp': random.randint(low, high)
    }
 
def assign_type_keywords(description: str) -> str:
    if not description:
        return "General"
    text = description.lower()
    for tipo, keywords in TIPOS_ES.items():
        if keywords and any(word in text for word in keywords):
            return tipo
    return "General"
  
def assign_type(description: str, title: str = "") -> str:
    category = assign_type_keywords(description)
    if category != "General":
        return category
    try:
        return _classifier.classify(title, description or "", list(TIPOS_ES.keys()))
    except Exception as e:
        print(f"Error en clasificación IA: {e}")
        return "General"
   
def generate_card():
    article = get_random_article()
    card_rarity = rarity(article["title"])
    stats = generate_stats(card_rarity)
    category = assign_type(article["category"])
    
    print(f'generando carta con rareza {card_rarity}, {stats}')
    
    dict = {
        "title": article["title"],
        "description":  article["description"],
        "image": article["image"],
        "rarity": card_rarity,
        "url": article["url"],
        "category": category,
        **stats
    }
    
    return CardModel.get_or_create_card(article['id'], **dict)

def generate_pack(size: int = 5) -> list[CardModel]:
    articles = [get_random_article() for _ in range(size)]
    categories = list(TIPOS_ES.keys())
    
    # Clasificar primero con keywords
    results = {}
    to_classify = []

    for i, article in enumerate(articles):
        category = assign_type_keywords(article["category"])
        if category != "General":
            results[i] = category
            print(f"✅ '{article['title']}' clasificado por keywords: {category}")
        else:
            to_classify.append((i, article))
            print(f"🤖 '{article['title']}' sin keywords, se preguntará a la IA")

    # Solo llamar a la IA con los que no se pudieron clasificar
    if to_classify:
        ai_input = [{"title": a["title"], "description": a["category"] or ""} for _, a in to_classify]
        ai_categories = _classifier.classify_batch(ai_input, categories)
        for (i, _), category in zip(to_classify, ai_categories):
            results[i] = category

    cards = []
    for i, article in enumerate(articles):
        card_rarity = rarity(article["title"])
        stats = generate_stats(card_rarity)
        card = CardModel.get_or_create_card(article["id"],
            title=article["title"],
            description=article["description"],
            image=article["image"],
            rarity=card_rarity,
            url=article["url"],
            category=results[i],
            **stats
        )
        cards.append(card)

    return cards

def generate_card_by_title(title: str) -> CardModel | None:
    card = CardModel.get_by_title(title)
    if card:
        print(f"✅ '{title}' encontrada en la DB")
        return card

    # 2. Si no está, buscar en Wikipedia
    print(f"🔍 '{title}' no está en la DB, buscando en Wikipedia...")
    article = get_article_by_title(title)
    if not article:
        return None

    card_rarity = rarity(article["title"])
    stats = generate_stats(card_rarity)
    category = assign_type(article["category"], article["title"])

    return CardModel.get_or_create_card(article["id"],
        title=article["title"],
        description=article["description"],
        image=article["image"],
        rarity=card_rarity,
        url=article["url"],
        category=category,
        **stats
    )