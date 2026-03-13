import random
from .wiki_api import get_random_article, get_wikipedia_categories
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
   
def assign_type(description: str, title : str = "") -> str:
    if not description:
        return "General"
    text = f"{description}".lower()
    for type, keywords in TIPOS_ES.items():
        if any(word in text for word in keywords):
            return type
    try:
        print("preguntando a la IA")
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
    
    return CardModel(
        wikipedia_id=article["id"],
        title= article["title"],
        description= article["description"],
        image= article["image"],
        rarity= card_rarity,
        url= article["url"],
        category= category,
        **stats
    )