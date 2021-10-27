from discord.ext import commands
from discord import embeds
import discord


class Channels(commands.Cog, name="Channels"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def add_channel(self, ctx, cat : str, chnl : str):
        category = discord.utils.get(ctx.guild.categories, name=cat)
        await ctx.guild.create_text_channel(chnl, category=category)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def add_voice(ctx, cat, chnl):
        category = discord.utils.get(ctx.guild.categories, name=cat)
        await ctx.guild.create_voice_channel(chnl, overwrites=None, category=category, reaspn=None)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(ctx, cat, chnl):
        category = discord.utils.get(ctx.guild.categories, name=cat)
        await ctx.guild.delete_text_channel(chnl, overwrites=None, category=category, reaspn=None)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def add_category(self,ctx,chnl, name):
        """
            adds channels
        """
        guild = self.bot.get_guild(ctx.guild.id)
        category = await guild.create_category(name, overwrites=None, reason=None)
        await ctx.guild.create_text_channel(chnl, category=category)


def setup(bot: commands.Bot):
    bot.add_cog(Channels(bot))
