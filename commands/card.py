from discord.ext import commands
import discord
from systems.card_dc_generator import gen_dc_card

class Card(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="card", help="Genera una carta aleatoria basada en un artículo de Wikipedia")
    async def card(self, ctx):
        print(f'Comando !card invocado por {ctx.author}...')
        card = gen_dc_card()
        await ctx.send(embed=card)
        
async def setup(bot):
    await bot.add_cog(Card(bot))