from dataclasses import dataclass, field
from typing import Optional
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
    id: Optional[int] = field(default=None)
    
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
    def _from_dict(cls, data: dict):
        """Construye un CardModel desde un dict de la DB, ignorando claves extra."""
        fields = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in data.items() if k in fields})
    
    @classmethod
    def get_or_create_card(cls, wikipedia_id, **kwargs):
        print("Consultando si existe")
        card_data = get_card(wikipedia_id) 
        if card_data:
            print("ya existe")
            return cls._from_dict(card_data)
        
        print("no existe")
        print("kwargs:", kwargs)
        new_card = cls( id=None, wikipedia_id=wikipedia_id, **kwargs)
        print(f"Creando carta {new_card}")
        new_card.save()
        card_data = get_card(wikipedia_id)
        if card_data is None:
            print(f"No se pudo recuperar la carta insertada")
            raise ValueError(f"No se pudo recuperar la carta después de insertarla: {wikipedia_id}")
        return cls._from_dict(card_data)