import os
import requests
import discord
import json
from discord.ext import commands

class Telegram(commands.Cog,name="Telegram"):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    global last_update_id
    last_update_id = 0
    with open('./assets/secrets.json', 'r') as f:
        secrets = json.load(f)
    with open('./assets/servers.json','r') as k:
        global servers
        servers=json.load(k)
    global key2
    key2 = secrets['telegram']
    
    @commands.Cog.listener()
    async def on_message(self,message):
        substring = "@everyone"
        channel = self.bot.get_channel(816266770204983307)
        for key in servers['data']:
            if 'MainAnnouncement' in servers['data'][key]:
                channel = self.bot.get_channel(
                    servers['data'][key]['MainAnnouncement'])
                if message.channel == channel:
                    if substring in message.content:
                        params = {
                            'chat_id': servers['data'][key]['Telegram'],
                            'text': message.content
                        }
                        url = f"https://api.telegram.org/bot{key2}/sendMessage"
                        r = requests.get(url, params=params)

        else:
            print("no")

def setup(bot:commands.Bot):
    bot.add_cog(Telegram(bot))
