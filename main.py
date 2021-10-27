
import discord
import os
import json
from discord.ext import commands
from keep_alive import keep_alive

with open('./assets/secrets.json', 'r') as f:
    secrets = json.load(f)
with open('./assets/data.json', 'r') as k:
    db = json.load(k)


def get_prefix(client, message):
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
        if str(message.guild.id) in servers['data']:
            return commands.when_mentioned_or(servers['data'][str(message.guild.id)]['prefix'])(client,message)
        return '.'


global last_update_id
last_update_id = 0
intents = discord.Intents().all()
intents.members = True
my_secret = secrets['token']





client = commands.Bot(command_prefix=get_prefix, intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Coding Myself to Death..'))
    # new_post.start()
    print('We have logged in as {0.user}'.format(client))





for folder in os.listdir("cogs"):
    if os.path.exists(os.path.join("cogs",folder,"cog.py")):
        client.load_extension(f"cogs.{folder}.cog")

keep_alive()
client.run(my_secret)
