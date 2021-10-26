import discord,json
import urllib.request
import datetime
import os
from discord.ext import commands, tasks



class News(commands.Cog,name="News"):
    def __init__(self,bot : commands.Bot):
        self.bot=bot
        self.new_post.start()
    with open('./assets/secrets.json', 'r') as f:
        secrets = json.load(f)
    global db
    with open('./assets/data.json', 'r') as k:
        db = json.load(k)
    global url
    url = secrets["facebook"]
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    latest_post = data['data'][0]['created_time']
    global format
    format = '%Y-%m-%dT%H:%M:%S'
    d1 = datetime.datetime.strptime(db["date"], format)

    @commands.command()
    async def latest(self,ctx):
        channel = self.bot.get_channel(ctx.channel.id)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        latest_post2 = data['data'][0]['created_time']
        datetime2 = datetime.datetime.strptime(
            latest_post2[:latest_post2.index('+')], format)
        print(latest_post2)
        embed = discord.Embed(
            title='Latest Announcement',
            description=data['data'][0]['message'],
            colour=discord.Colour.blue()
        )
        embed.set_footer(text='time added :' +
                        datetime2.strftime('%Y-%m-%d AT %H:%M:%S'))
        print('yes')
        if 'attachments' in data['data'][0] and 'subattachments'not in data['data'][0]['attachments']['data'][0]:
            embed.set_image(url=data['data'][0]['attachments']
                            ['data'][0]['media']['image']['src'])
        await ctx.send(embed=embed)
        if 'subattachments' in data['data'][0]['attachments']['data'][0]:
            for data in data['data'][0]['attachments']['data'][0]['subattachments']['data']:
                embed = discord.Embed(
                    colour=discord.Colour.blue()
                )
                embed.set_image(url=data['media']['image']['src'])
                await ctx.send(embed=embed)
    global channel
    
    @tasks.loop(seconds=30)
    async def new_post(self):
        with open('./assets/servers.json','r') as an:
            servers = json.load(an)
        for key in servers['data'].keys():
            if 'MainAnnouncement' in servers['data'][key]:
                channel = self.bot.get_channel(
                    servers['data'][key]['MainAnnouncement'])
                if not channel :
                    return
                guild = self.bot.get_guild(896118007422656633)
                response = urllib.request.urlopen(url)
                data = json.loads(response.read())
                latest_post2 = data['data'][0]['created_time']
                datetime2 = datetime.datetime.strptime(
                    latest_post2[:latest_post2.index('+')], format)

                global d1
                d1 = datetime.datetime.strptime(db['date'], format)
                if datetime2 > d1:
                    embed = discord.Embed(
                        title='New Announcement',
                        description=data['data'][0]['message'],
                        colour=discord.Colour.blue()
                    )

                    embed.set_footer(text='time added :' +
                                    datetime2.strftime('%Y-%m-%d AT %H:%M:%S'))       
                    if 'attachments' in data['data'][0] and 'subattachments'not in data['data'][0]['attachments']['data'][0]:
                        embed.set_image(url=data['data'][0]['attachments']
                                        ['data'][0]['media']['image']['src'])

                    # await channel.send(guild.default_role)
                    await channel.send(embed=embed)
                    if 'attachments' in data['data'][0]:
                        if 'subattachments' in data['data'][0]['attachments']['data'][0]:
                            for data in data['data'][0]['attachments']['data'][0]['subattachments']['data']:
                                embed = discord.Embed(
                                    colour=discord.Colour.blue()
                                )
                                embed.set_image(url=data['media']['image']['src'])
                                await channel.send(embed=embed)
                    d1 = datetime2
                    db["date"] = d1.strftime(format)

                    with open('./assets/data.json', 'w') as l :
                        json.dump(db,l,indent=4)

def setup(bot:commands.Bot):
    bot.add_cog(News(bot))
