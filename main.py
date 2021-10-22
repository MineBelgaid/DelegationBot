from logging import exception
import discord
import os
import urllib
import json
import datetime
import urllib.request
import json
import os
import asyncio
import youtube_dl

from discord import embeds
from discord.ext import commands, tasks
from keep_alive import keep_alive
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageDraw


with open('./assets/secrets.json', 'r') as f:
    secrets = json.load(f)
with open('./assets/data.json', 'r') as k:
    db = json.load(k)


def get_prefix(client, message):
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
        return servers['data'][str(message.guild.id)]['prefix']


im1 = Image.open('./assets/images/welcome.png')
intents = discord.Intents().all()
intents.members = True
my_secret = secrets['token']
url = secrets['facebook']
response = urllib.request.urlopen(url)
data = json.loads(response.read())

client = commands.Bot(command_prefix=commands.when_mentioned_or(
    "."), intents=intents)


latest_post = data['data'][0]['created_time']
format = '%Y-%m-%dT%H:%M:%S'
d1 = datetime.datetime.strptime(db["date"], format)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Coding Myself to Death..'))
    new_post.start()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_guild_join(guild):
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
        servers["data"][str(guild.id)] = {"prefix": "."}
        f.seek(0)
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)


@client.event
async def on_guild_leave(guild):
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
    servers['data'].pop([str(guild.id)])
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)


@client.command()
async def setprefix(ctx, prefix):
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
        servers['data'][str(ctx.guild.id)]['prefix'] = prefix
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)
    await ctx.send(f'Prefix changed to {prefix}')


@client.command()
async def setwelcome(ctx):
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
        servers['data'][str(ctx.guild.id)]['welcome'] = ctx.channel.id
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

    await ctx.send('This channel has been set as **Welcome Channel**!')


@client.command()
async def setannouncements(ctx):
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
        servers['data'][str(ctx.guild.id)]['announcements'] = ctx.channel.id
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)
    await ctx.send('This channel has been set as **Announcements Channel**!')


@client.command()
async def setdeleted(ctx):
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
        servers['data'][str(ctx.guild.id)]['deleted'] = ctx.channel.id
    with open('./assets/servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

    await ctx.send('This channel has been set as **Deleted Messages Channel**!')


@client.command()
async def ping(ctx):
    embed = discord.Embed(
        title='Claim your roles!',
        description=':one: : Group 1\n\n:two: : Group 2\n\n:three: : Group 3\n\n :four: : Group 4!\n',
        colour=discord.Colour.blue()

    )
    embed.set_footer(text="React with the Emoji corresponding to your group!")
    await ctx.send(embed=embed)


@client.event
async def on_member_join(member):
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
    guild = client.get_guild(member.guild.id)
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
        output.save('./assets/images/output.png')
        back_im = im1.copy()
        back_im.paste(im, (20, 0))
        back_im.save('./assets/images/welcome2.png')
        file = discord.File("./assets/images/welcome2.png",
                            filename="welcome2.png")
        embed.set_image(url="attachment://welcome2.png")
        await channel.send(embed=embed, file=file)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)


@client.command()
async def mute(ctx, member: discord.Member = None, time=0, *, unit, reason=None):
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


@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member = None, *, reason=None):
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



# Voice commands


@client.command()
async def join(ctx):
    user = ctx.message.author
    vc = user.voice.channel
    voice = discord.utils.get(client.voice_clients,guild =ctx.guild)
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!")
    voice_channel = ctx.author.voice.channel
    if voice is None:
        await vc.connect()
        await ctx.send("Delegation has arrived to the channel!")
    else:
        await ctx.send("I'm already in an existing channel")


@client.command()
async def disconnect(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Succesfully left the channel ! ")
    else :
        await ctx.send("I am not connected") 

@client.command()
async def pause(ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused ! ")
    

@client.command()
async def resume(ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resumed ! ")

@client.command()
async def play(ctx, url):
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': "bestaudio"}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, ** FFMPEG_OPTIONS)
        vc.play(source)
        ctx.send("Now playing ")


@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:

        pass

    else:
        with open('./assets/reactions.json') as f:
            data = json.load(f)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['msg_id'] == str(payload.message_id):
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])
                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('./assets/reactions.json') as f:
        data = json.load(f)
        for x in data:
            if x['emoji'] == payload.emoji.name and x['msg_id'] == str(payload.message_id):
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])
                await client.get_guild(
                    payload.guild_id).get_member(payload.user_id).remove_roles(role)


@client.command()
async def autorole(ctx, emoji, role: discord.Role, *, msgId):
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


@client.command()
async def latest(ctx):
    channel = client.get_channel(ctx.channel.id)
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


@client.command()
async def all(ctx):
    await ctx.send(ctx.message.guild.default_role)


@tasks.loop(seconds=30)
async def new_post():
    channel = client.get_channel(896142603437899807)
    guild = client.get_guild(896118007422656633)
    response = urllib.request.urlopen(url)
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


@client.command()
async def setup_counter(ctx, name, chnl):
    guild = client.get_guild(ctx.guild.id)
    category = await guild.create_category(name, overwrites=None, reason=None)
    await ctx.guild.create_text_channel(chnl, category=category)


@client.command()
async def add_channel(ctx, cat, chnl):
    category = discord.utils.get(ctx.guild.categories, name=cat)
    await ctx.guild.create_text_channel(chnl, category=category)


@client.command()
async def add_voice(ctx, cat, chnl):
    category = discord.utils.get(ctx.guild.categories, name=cat)
    await ctx.guild.create_voice_channel(chnl, overwrites=None, category=category, reaspn=None)


@client.command()
async def delete_channel(ctx, cat, chnl):
    category = discord.utils.get(ctx.guild.categories, name=cat)
    await ctx.guild.delete_text_channel(chnl, overwrites=None, category=category, reaspn=None)


@client.event
async def on_message_delete(message):
    msg = str(message.author) + ' deleted a message'
    embed = discord.Embed(
        description=f'Channel : <#{message.channel.id}>',

        title=str(msg)
    )
    embed.add_field(name="Message deleted ",
                    value=f"```{str(message.content)}```")
    with open('./assets/servers.json', 'r') as f:
        servers = json.load(f)
        deleted = servers['data'][str(message.guild.id)]['deleted']
        channel = client.get_channel(deleted)
    await channel.send(embed=embed)
keep_alive()
client.run(my_secret)
