import discord,json
from discord.ext import commands
class Roles(commands.Cog,name="Roles"):
    def __init__(self,bot:commands.Bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.member.bot:

            pass

        else:
            with open('./assets/reactions.json') as f:
                data = json.load(f)
                for x in data:
                    if x['emoji'] == payload.emoji.name and x['msg_id'] == str(payload.message_id):
                        role = discord.utils.get(self.bot.get_guild(
                            payload.guild_id).roles, id=x['role_id'])
                        await payload.member.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        with open('./assets/reactions.json') as f:
            data = json.load(f)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['msg_id'] == str(payload.message_id):
                    role = discord.utils.get(self.bot.get_guild(
                        payload.guild_id).roles, id=x['role_id'])
                    await self.bot.get_guild(
                        payload.guild_id).get_member(payload.user_id).remove_roles(role)


    @commands.command()
    async def autorole(self, ctx, emoji, role: discord.Role, *, msgId):
        msg = await ctx.fetch_message(msgId)
        await msg.add_reaction(emoji)
        with open('./assets/reactions.json') as f:
            reactions = json.load(f)
            new_reaction = {
                'role_name': role.name,
                'role_id': role.id,
                'emoji': emoji,
                'msg_id': msgId
            }
            reactions.append(new_reaction)
        with open('./assets/reactions.json', 'w') as f:
            json.dump(reactions, f, indent=4)


def setup(bot:commands.Bot):
    bot.add_cog(Roles(bot))