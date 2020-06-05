import discord
from discord.ext import commands
import asyncio
import random
from discord import client, guild, member
from random import randint, choice
import threading
import time
import datetime
import os
from time import sleep
import io
import random as r
from discord.utils import get
from discord.voice_client import VoiceClient
import youtube_dl
import ffmpeg
from ffmpeg import *


prefix = '!'

Bot = commands.Bot(command_prefix= prefix)

Bot.remove_command('help')

@Bot.command(pass_context = True)
async def инфо(ctx):
    emb = discord.Embed(title= "Информация о коммандах:globe_with_meridians:",colour= 0xfbfcfe)
    emb.add_field(name = "{}инфо".format(prefix), value= "**Показывает все команды**" )
    await ctx.send(embed= emb)
    emb = discord.Embed(title= "Игры:video_game:", colour= 0x8B8989)
    emb.add_field(name = "{}кнб".format(prefix), value= "**Играть в камень/ножницы/бумага с ботом**")
    emb.add_field(name = "{}играть".format(prefix), value= "**В орел и решка**", inline=False)
    await ctx.send(embed= emb)
    emb = discord.Embed(title= "Инструменты(Админ):tools:", colour= 0x8B8989)
    emb.add_field(name = "{}очистить".format(prefix), value= "**Чистит чат от 1/10000**", inline=False)
    emb.add_field(name = "{}mute".format(prefix), value= "**Запретит участнику писать,говорить**")
    emb.add_field(name = "{}unmute".format(prefix), value= "**Разрешить участнику писать,говорить**")
    emb.add_field(name = "{}ban".format(prefix),  value= "**Банит участника**", inline=False)   
    await ctx.send(embed= emb)
    emb = discord.Embed(title= "Плюшки:smiling_face_with_3_hearts:", colour= 0x8B8989)
    emb.add_field(name = "{}стат".format(prefix), value= "**Просмотр своей(чужой) статистики сообщений**")
    emb.add_field(name = "{}аватар".format(prefix), value= "**Показ автарки указанного участника**", inline=False)
    emb.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed= emb)
    

#------------------------------------------------------------------------------------------------------------------------#
@Bot.event
async def on_ready():
    print('online!')
    game = discord.Game(r"!инфо")
    await Bot.change_presence(status=discord.Status.online, activity=game)

#------------------------------------------------------------------------------------------------------------------------#

@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(718334578141560854)
    role = discord.utils.get(member.guild.roles, id= 713476934226673795)
    await member.add_roles(role)
    await channel.send(embed = discord.Embed(description = f'''📢Пользователь ``{member}`` присоеденился📢''', color=0x0c0c0c))

#------------------------------------------------------------------------------------------------------------------------#

@Bot.event
async def on_member_remove(member):
    channel = Bot.get_channel(718334608026107994)
    role = discord.utils.get(member.guild.roles, id= 6713476531300860055)
    await member.remove_roles(role)
    await channel.send(embed = discord.Embed(description = f'''📢Пользователь ``{member}`` отключился📢''', color=0x0c0c0c))

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
@commands.has_permissions(administrator= True)
async def mute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name= "Мут")
    await member.add_roles(mute_role)
    author = ctx.message.author
    await ctx.send(f"Человек был успешно замучен!:white_check_mark: {author.mention}")

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
@commands.has_permissions(administrator= True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name= "Мут")
    await member.remove_roles(mute_role)
    author = ctx.message.author
    await ctx.send(f"Человек был успешно размучен!:white_check_mark: {author.mention}")

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
async def играть(ctx):
    """Играть с ботом"""
    num=random.randint(1,2)
    if (num == 1):
           await ctx.send("Вым выпал :dollar: Орёл")
           print("[?coin] - done")
    if(num == 2):    
           await ctx.send("Вам выпала :yen: Решка")
           print("[?coin - done")
#------------------------------------------------------------------------------------------------------------------------#
@Bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def очистить(ctx, amount = 1000):
    """Чистка чата"""
    await ctx.message.delete() # Удаляет написанное вами сообщение
    await ctx.channel.purge(limit = amount) #удаляет сообщения
    em = discord.Embed(description= f'было удаленно *{amount}* сообщений', color = 708090) #настройка embed
    await ctx.send(embed=em) #вставка embed
    await asyncio.sleep(1) #таймер ожидания
    await ctx.channel.purge(limit = 1) # Удаляет сообщение бота
class Messages:
    def __init__(self, Bot):
        self.Bot = Bot
    async def number_messages(self, member):
        n_messages = 0
        for guild in self.Bot.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit = None):
                        if message.author == member:
                            n_messages += 1
                except (discord.Forbidden, discord.HTTPException):
                    continue
        return n_messages
#------------------------------------------------------------------------------------------------------------------------#
@Bot.command(name = "стат")
async def num_msg(ctx, member: discord.Member = None):
    """Счетчик сообщний"""
    user = ctx.message.author if (member == None) else member
    number = await Messages(Bot).number_messages(user)
    embed = discord.Embed(description = f"Количество сообщений на сервере от **{user.name}** — **{number}**!")
    await ctx.send(embed = embed)
#------------------------------------------------------------------------------------------------------------------------#
@Bot.command()
async def кнб(ctx, move: str = None):
    solutions = ["`ножницы`", "`камень`", "`бумага`"]
    winner = "**НИЧЬЯ**"
    p1 = solutions.index(f"`{move.lower()}`")
    p2 = randint(0, 2)
    if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0:
        winner = f"{ctx.message.author.mention} ты **Проиграл**"
    elif p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1 or p1 == 0 and p2 == 2:
        winner = f"{ctx.message.author.mention} ты **Выиграл**"
    await ctx.send(    
        f"{ctx.message.author.mention} **=>** {solutions[p1]}\n"
        f"{Bot.user.mention} **=>** {solutions[p2]}\n"
        f"{winner}")

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member : discord.Member, reason=None):
    if reason == None:
        await ctx.send(f"Воу {ctx.author.mention}, введи причину для этого!")
    else:
        messageok = f"Ты был за забнанен на {ctx.guild.name} по причине {reason}"
        await ctx.send(f"{ctx.author.mention} Человек был успешно забанен!:white_check_mark:")
        await member.send(messageok)
        await member.ban(reason=reason)

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
async def аватар(ctx, member : discord.Member = None):
    user = ctx.message.author if (member == None) else member
    await ctx.message.delete()
    embed = discord.Embed(title=f'Аватар пользователя {user}', description= f'[Ссылка на изображение]({user.avatar_url})', color=user.color)
    embed.set_footer(text= f'Вызвано: {ctx.message.author}', icon_url= str(ctx.message.author.avatar_url))
    embed.set_image(url=user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member : discord.Member, reason=None):
    if reason == None:
        await ctx.send(f"Воу {ctx.author.mention}, введи причину для этого!")
    else:
        messageok = f"Ты был за забнанен на {ctx.guild.name} по причине {reason}"
        await ctx.send(f"{ctx.author.mention} Человек был успешно забанен!:white_check_mark:")
        await member.send(messageok)
        await member.kick(reason=reason)

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
    except PermissionError:
        print('Не удалось удалить файл')

    await ctx.send('Секундочку бот загружает песню...')
    voice = get(Bot.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExctractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас играет: {song_name[0]}')



#------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------#

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
