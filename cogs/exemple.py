import discord
import os
import urllib
import json
import datetime
import urllib.request
import json
import os
from discord import embeds
from discord.ext import commands, tasks
from keep_alive import keep_alive
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageDraw

with open('./assets/secrets.json', 'r') as f:
    secrets = json.load(f)
with open('./assets/data.json', 'r') as k:
    db = json.load(k)

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = secrets['facebook']
        self.response = urllib.request.urlopen(self.url)
        self.data = json.loads(self.response.read())
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game('Coding Myself to Death..'))
        self.new_post.start()
        print('We have logged in as {0.user}'.format(self.client))
    
    @commands.command()
    async def setprefix(ctx, prefix):
        with open('./assets/servers.json', 'r') as f:
            servers = json.load(f)
            servers['data'][str(ctx.guild.id)]['prefix'] = prefix
        with open('servers.json', 'w') as f:
            json.dump(servers, f, indent=4)
        await ctx.send(f'Prefix changed to {prefix}')

    @tasks.loop(seconds=30)
    async def new_post(self):
        channel = self.client.get_channel(896142603437899807)
        guild = self.client.get_guild(896118007422656633)
        response = urllib.request.urlopen(self.url)
        data = json.loads(response.read())
        latest_post2 = data['data'][0]['created_time']
        datetime2 = datetime.datetime.strptime(
            latest_post2[:latest_post2.index('+')], format)

        global d1
        d1 = datetime.datetime.strptime(db["data"], format)
        print()
        if datetime2 > d1:
            d1 = datetime2
            db["data"] = d1.strftime(format)
            embed = discord.Embed(
                title='New Announcement',
                description=data['data'][0]['message'],
                colour=discord.Colour.blue()
            )

            embed.set_footer(text='time added :' +
                            datetime2.strftime('%Y-%m-%d AT %H:%M:%S'))
            print('yes')
            if 'attachments' in data['data'][0] and 'subattachments'not in data['data'][0]['attachments']['data'][0]:
                embed.set_image(url=data['data'][0]['attachments']
                                ['data'][0]['media']['image']['src'])

            await channel.send(guild.default_role)
            await channel.send(embed=embed)
            if 'subattachments' in data['data'][0]['attachments']['data'][0]:
                for data in data['data'][0]['attachments']['data'][0]['subattachments']['data']:
                    embed = discord.Embed(
                        colour=discord.Colour.blue()
                    )
                    embed.set_image(url=data['media']['image']['src'])
                    await channel.send(embed=embed)
        else:
            print("not")





def setup(client):
    client.add_cog(Example(client))
