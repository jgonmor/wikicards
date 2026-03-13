from dataclasses import dataclass
from ..tcg_api import insert_card, get_card

@dataclass
class CardModel:
    wikipedia_id: str
    title: str
    description: str
    image: str
    rarity: str
    attack: int
    defense: int
    hp: int
    category: str
    url: str
    
    def save(self):
        print("Guardando carta")
        insert_card(
            self.wikipedia_id,
            self.title,
            self.description,
            self.image,
            self.rarity,
            self.attack,
            self.defense,
            self.hp,
            self.category,
            self.url
        )
        print("Carta guardada")
        
    @classmethod
    def get_or_create_card(cls, wikipedia_id, **kwargs):
        print("Consultando si existe")
        card_data = get_card(wikipedia_id) 
        if card_data:
            print("ya existe")
            return cls(
                wikipedia_id=card_data["wikipedia_id"],
                title=card_data["title"],
                description=card_data["description"],
                image=card_data["image"],
                rarity=card_data["rarity"],
                attack=card_data["attack"],
                defense=card_data["defense"],
                hp=card_data["hp"],
                category=card_data["category"],
                url=card_data["url"]
            )
        
        print("no existe")
        print("kwargs:", kwargs)
        new_card = cls(wikipedia_id=wikipedia_id, **kwargs)
        print(f"Creando carta {new_card}")
        new_card.save()
        
        return new_card