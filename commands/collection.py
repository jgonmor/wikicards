from discord.ext import commands
import discord
from database.models.player_model import PlayerModel
from systems.card_dc_generator import card_to_embed

RARITY_EMOJI = {
    "Común":      "⚪",
    "Raro":       "🔵",
    "Épico":      "🟣",
    "Legendario": "🟡",
    "Mítico":     "🔴"
}

def build_collection_embed(cards: list, username: str) -> discord.Embed:
    embed = discord.Embed(
        title=f"📚 Colección de {username}",
        description=f"Tienes **{len(cards)}** cartas.",
        color=discord.Color.blurple()
    )
    for rarity, emoji in RARITY_EMOJI.items():
        rarity_cards = [c for c in cards if c.rarity == rarity]
        if rarity_cards:
            embed.add_field(
                name=f"{emoji} {rarity} ({len(rarity_cards)})",
                value="\n".join([
                    f"• {c.title} — {c.category} x{c.quantity}"
                    for c in rarity_cards
                ]),
                inline=False
            )
    return embed

class CardButton(discord.ui.Button):
    def __init__(self, card):
        emoji = RARITY_EMOJI.get(card.rarity, "⚪")
        super().__init__(
            label=f"{emoji} {card.title[:40]}",
            style=self._rarity_style(card.rarity),
            custom_id=f"card_{card.id}"
        )
        self.card = card

    def _rarity_style(self, rarity: str) -> discord.ButtonStyle:
        styles = {
            "Común":      discord.ButtonStyle.secondary,
            "Raro":       discord.ButtonStyle.primary,
            "Épico":      discord.ButtonStyle.primary,
            "Legendario": discord.ButtonStyle.success,
            "Mítico":     discord.ButtonStyle.danger
        }
        return styles.get(rarity, discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=card_to_embed(self.card), ephemeral=True)

class CollectionView(discord.ui.View):
    def __init__(self, cards: list):
        super().__init__(timeout=60)
        for card in cards[:25]:
            self.add_item(CardButton(card))

class Collection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="collection", help="Muestra tu colección")
    async def collection_public(self, ctx):
        player = PlayerModel.get_or_create(str(ctx.author.id), ctx.author.name)
        cards = player.get_collection()

        if not cards:
            await ctx.send("No tienes cartas todavía. Usa !card o !pack para conseguir algunas.")
            return

        embed = build_collection_embed(cards, ctx.author.name)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Collection(bot))