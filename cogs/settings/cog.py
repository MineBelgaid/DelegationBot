import json,discord
import asyncio,os
from discord.ext import commands

class Settings(commands.Cog,name="Server Settings"):
    def __init__(self,bot:commands.Bot):
        self.bot=bot
    @commands.command()
    async def setprefix(self,ctx, prefix):
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
            servers['data'][str(ctx.guild.id)]['prefix'] = prefix
        with open('./assets/servers.json', 'w') as f:
            json.dump(servers, f, indent=4)
        await ctx.send(f'Prefix changed to {prefix}')


    @commands.command()
    async def setwelcome(self,ctx):
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
            servers['data'][str(ctx.guild.id)]['welcome'] = ctx.channel.id
        with open('./assets/servers.json', 'w') as f:
            json.dump(servers, f, indent=4)

        await ctx.send('This channel has been set as **Welcome Channel**!')


    @commands.command()
    async def setannouncements(self,ctx):
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
            servers['data'][str(ctx.guild.id)]['announcements'] = ctx.channel.id
        with open('./assets/servers.json', 'w') as f:
            json.dump(servers, f, indent=4)
        await ctx.send('This channel has been set as **Announcements Channel**!')
    @commands.command()
    async def setmain(self,ctx):
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
            servers['data'][str(ctx.guild.id)
                            ]['MainAnnouncement'] = ctx.channel.id
        with open('./assets/servers.json', 'w') as f:
            json.dump(servers, f, indent=4)
        await ctx.send('This channel has been set as **Main Announcements Channel**!')


    @commands.command()
    async def setdeleted(self, ctx):
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
            servers['data'][str(ctx.guild.id)]['deleted'] = ctx.channel.id
        with open('./assets/servers.json', 'w') as f:
            json.dump(servers, f, indent=4)

        await ctx.send('This channel has been set as **Deleted Messages Channel**!')


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self,ctx, member: discord.Member = None, time=0, *, unit, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, id=898548577259892807)
        if not member:
            await ctx.send("You must choose a user!")
        elif not time:
            await ctx.send("You must give a time")

        embed = discord.Embed(title="muted ",
                            description=f"{member.mention} has been muted")
        embed.add_field(name="Reason: ", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        if unit == "s":
            wait = 1 * time
            await asyncio.sleep(wait)
        elif unit == "m":
            wait = 60 * time
            await asyncio.sleep(wait)
        await member.remove_roles(mutedRole)
        embed = discord.Embed(title="muted ",
                            description=f"{member.mention} has been unmuted")
        embed.add_field(name="Reason: ", value=reason, inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member = None, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, id=898548577259892807)
        if not member:
            await ctx.send("You must choose a memeber!")
        else:
            embed = discord.Embed(
                title="Unmuted ", description=f"{member.mention} has been unmuted")
            embed.add_field(name="Reason: ", value=reason, inline=False)
            await member.remove_roles(mutedRole)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        msg = str(message.author) + ' deleted a message'
        embed = discord.Embed(
            description=f'Channel : <#{message.channel.id}>',

            title=str(msg)
        )
        embed.add_field(name="Message deleted ",
                        value=f"```{str(message.content)}```")
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
        if 'deleted' in servers['data'][str(message.guild.id)]:
            deleted = servers['data'][str(message.guild.id)]['deleted']
            channel = self.bot.get_channel(deleted)
            await channel.send(embed=embed)


def setup(bot:commands.Bot):
    bot.add_cog(Settings(bot))
