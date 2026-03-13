from discord.ext import commands
import discord
from systems.card_dc_generator import gen_dc_card

class Pack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pack", help="Genera un sobre con 5 cartas")
    async def pack(self, ctx):
        print(f'Comando !pack invocado por {ctx.author}...')
        for i in range(5):
            card = gen_dc_card()
            await ctx.send(embed=card)
        
    def rarityColor(self, rarity):
        ranges = {
            "Común": discord.Color.green(),
            "Raro": discord.Color.blue(),
            "Épico": discord.Color.pink(),
            "Legendario": discord.Color.purple(),
            "Mítico": discord.Color.gold()
        }
        print(f"Color seleccionado: {ranges[rarity]}")
        return ranges[rarity]
        
async def setup(bot):
    await bot.add_cog(Pack(bot))