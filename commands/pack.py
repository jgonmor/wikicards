from discord.ext import commands
import discord
from systems.card_dc_generator import card_to_embed
from systems.card_generator import generate_pack
from database.models.player_model import PlayerModel

class Pack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pack", help="Genera un sobre con 5 cartas")
    async def pack(self, ctx):
        print(f'Comando !pack invocado por {ctx.author}...')
        player = PlayerModel.get_or_create(str(ctx.author.id), ctx.author.name)
        cards = generate_pack(5)
        for card in cards:
            player.assign_card(card)
            await ctx.send(embed=card_to_embed(card))
        
async def setup(bot):
    await bot.add_cog(Pack(bot))