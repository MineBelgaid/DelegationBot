import json,discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageDraw
class Owner(commands.Cog,name="Owner"):
    def __init__(self,bot:commands.Bot):
        self.bot=bot
    global im1
    im1 = Image.open('./assets/images/welcome.png')
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
            servers["data"][str(guild.id)] = {"prefix": "."}
            f.seek(0)
        with open('./assets/servers.json', 'w') as f:
            json.dump(servers, f, indent=4)


    @commands.Cog.listener()
    async def on_guild_leave(self,guild):
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
        servers['data'].pop([str(guild.id)])
        with open('./assets/servers.json', 'w') as f:
            json.dump(servers, f, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
        guild = self.bot.get_guild(member.guild.id)
        role = discord.utils.get(member.guild.roles, name='Membre')
        await member.add_roles(role)
        if 'welcome' in servers['data'][str(member.guild.id)]:
            channel = guild.get_channel(
                servers['data'][str(member.guild.id)]['welcome'])
            print(member.avatar_url)
            await member.avatar_url.save("./assets/images/logo.png")
            embed = discord.Embed(
                title=f'Our Newest Geek! :spy:',
                description=f'{member.mention} ',
                colour=discord.Colour.blue(),
            )
            im = Image.open("./assets/images/logo.png")
            im = im.resize((120, 120))
            bigsize = (im.size[0] * 3, im.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(im.size, Image.ANTIALIAS)
            im.putalpha(mask)
            output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            output.convert('RGB')
            output.save('./assets/images/output.png')
            back_im = im1.copy()
            back_im.paste(im, (20, 0))
            back_im.save('./assets/images/welcome2.png')
            file = discord.File("./assets/images/welcome2.png",
                                filename="welcome2.png")
            embed.set_image(url="attachment://welcome2.png")
            await channel.send(embed=embed, file=file)

def setup(bot:commands.Bot):
    bot.add_cog(Owner(bot))
