from discord.ext import commands
import discord
from systems.card_dc_generator import gen_dc_card
from database.models.player_model import PlayerModel

class Pack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pack", help="Genera un sobre con 5 cartas")
    async def pack(self, ctx):
        print(f'Comando !pack invocado por {ctx.author}...')
        player = PlayerModel.get_or_create(
            discord_id=str(ctx.author.id),
            username=ctx.author.name
        )
        for i in range(5):
            card, embed = gen_dc_card()
            player.assign_card(card)
            await ctx.send(embed=embed)
        
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