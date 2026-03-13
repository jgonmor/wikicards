from dataclasses import dataclass
from ..tcg_api import get_player, insert_player, assign_card_to_player, get_player_cards
from database.models.card_model import CardModel

@dataclass
class PlayerModel:
    id: int
    discord_id: str
    username: str

    def assign_card(self, card):
        """Añade una carta a la colección del jugador (o incrementa cantidad)."""
        assign_card_to_player(self.id, card.id)

    @classmethod
    def get_or_create(cls, discord_id: str, username: str):
        data = get_player(discord_id)
        if data:
            return cls(**data)
        insert_player(discord_id, username)
        data = get_player(discord_id)
        if data is None:
            raise ValueError(f"No se puede obtener el nuevo player")
        return cls(**data)
    
    def get_collection(self) -> list[CardModel]:
        cards_data = get_player_cards(self.id)
        return [CardModel._from_dict(c) for c in cards_data]