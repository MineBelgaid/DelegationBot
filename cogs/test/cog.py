from discord.ext import commands
from discord import embeds
import discord
class Ping(commands.Cog,name="Ping"):
    def __init__(self,bot : commands.Bot):
        self.bot=bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def ping(self,ctx:commands.Context):
        embed = discord.Embed(
            title='Claim your roles!',
            description=':one: : Group 1\n\n:two: : Group 2\n\n:three: : Group 3\n\n :four: : Group 4!\n',
            colour=discord.Colour.blue()

        )
        embed.set_footer(text="React with the Emoji corresponding to your group!")
        await ctx.send(embed=embed)
        
def setup(bot:commands.Bot):
    bot.add_cog(Ping(bot))
