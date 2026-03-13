from discord.ext import commands
import discord
from systems.card_dc_generator import gen_dc_card, card_to_embed
from systems.card_generator import generate_card_by_title
from database.models.player_model import PlayerModel

class Card(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="card", help="Genera una carta aleatoria o busca una por nombre")
    async def card(self, ctx, *, title: str = None): # type: ignore
        player = PlayerModel.get_or_create(str(ctx.author.id), ctx.author.name)

        if title:
            async with ctx.typing():
                card = generate_card_by_title(title)
            if not card:
                await ctx.send(f"❌ No se ha encontrado ningún artículo de Wikipedia para **{title}**.")
                return
            await ctx.send(embed=card_to_embed(card))
        else:
            card, embed = gen_dc_card()
            player.assign_card(card)
            await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Card(bot))