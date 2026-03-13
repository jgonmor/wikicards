from systems.card_generator import generate_card
import discord

def gen_dc_card():
    card = generate_card()
    print('carta obtenida para imprimir')
    embed = discord.Embed(
        title=card.title,
        description=card.description,
        color=rarityColor(card.rarity),
        url=card.url
    )
    print("Cabecera creada")
    embed.add_field(name="Rareza", value=card.rarity)
    embed.add_field(name="Categoria", value=card.category)
    embed.add_field(name="ATK", value=card.attack)
    embed.add_field(name="DEF", value=card.defense)
    embed.add_field(name="HP", value=card.hp)
    
    if card.image:
        embed.set_image(url=card.image)
        
    return card, embed
        
def rarityColor(rarity):
        ranges = {
            "Común": discord.Color.green(),
            "Raro": discord.Color.blue(),
            "Épico": discord.Color.pink(),
            "Legendario": discord.Color.purple(),
            "Mítico": discord.Color.gold()
        }
        print(f"Color seleccionado: {ranges[rarity]}")
        return ranges[rarity]