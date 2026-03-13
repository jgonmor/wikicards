from discord.ext import commands
import discord
from systems.card_dc_generator import gen_dc_card
from database.models.player_model import PlayerModel

class Card(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="card", help="Genera una carta aleatoria basada en un artículo de Wikipedia")
    async def card(self, ctx):
        print(f'Comando !card invocado por {ctx.author}...')
        player = PlayerModel.get_or_create(
            discord_id=str(ctx.author.id),
            username=ctx.author.name
        )
        card, embed = gen_dc_card()
        player.assign_card(card)
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Card(bot))