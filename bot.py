import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import bot
from discord import client, guild, member
from random import randint, choice
import threading
import time
import datetime
import os
from time import sleep
import io
import random as r



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
    emb.add_field(name = "{}очистить".format(prefix), value= "**Чистит чат от 1/10000**")
    emb.add_field(name = "{}mute".format(prefix), value= "**Запретит участнику писать,говорить**", inline=False)
    emb.add_field(name = "{}unmute".format(prefix), value= "**Разрешить участнику писать,говорить**")
    emb.add_field(name = "{}say".format(prefix), value= "**Отправлять сообщение от имени бота(с упоминанием человека)**", inline=False)
    emb.add_field(name = "{}ban".format(prefix),  value= "**Банит участника**", inline=False)
    emb.add_field(name = "{}gw".format(prefix),  value= "**Делает розыгрыш для участников сервера**")    
    await ctx.send(embed= emb)
    emb = discord.Embed(title= "Плюшки:smiling_face_with_3_hearts:", colour= 0x8B8989)
    emb.add_field(name = "{}стат".format(prefix), value= "**Просмотр своей(чужой) статистики сообщений**")
    emb.add_field(name = "{}аватар".format(prefix), value= "**Показ автарки указанного участника**", inline=False)
    await ctx.send(embed= emb)
    


@Bot.event
async def on_ready():
    print('online!')
    game = discord.Game(r"!инфо")
    await Bot.change_presence(status=discord.Status.online, activity=game)

@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(698660443291385906)
    role = discord.utils.get(member.guild.roles, id= 698514876313894993)
    await member.add_roles(role)
    await channel.send(embed = discord.Embed(description = f'''📢Пользователь ``{member}`` присоеденился📢''', color=0x0c0c0c))

@Bot.event
async def on_member_remove(member):
    channel = Bot.get_channel(698660443291385906)
    role = discord.utils.get(member.guild.roles, id= 698514876313894993)
    await member.remove_roles(role)
    await channel.send(embed = discord.Embed(description = f'''📢Пользователь ``{member}`` отключился📢''', color=0x0c0c0c))

@Bot.command()
@commands.has_permissions(administrator= True)
async def mute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name= "Мут")
    await member.add_roles(mute_role)
    author = ctx.message.author
    await ctx.send(f"Человек был успешно замучен!:white_check_mark: {author.mention}")

@Bot.command()
@commands.has_permissions(administrator= True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name= "Мут")
    await member.remove_roles(mute_role)
    author = ctx.message.author
    await ctx.send(f"Человек был успешно размучен!:white_check_mark: {author.mention}")

@Bot.command()
async def диаслох(ctx):
    author = ctx.message.author
    await ctx.send(f"Полностью согласен с вашем мнением!:white_check_mark: {author.mention}")

@Bot.command()
async def диас(ctx, member : discord.Member = None):
    author = ctx.message.author
    user = ctx.message.author if (member == None) else member
    await ctx.send(f"ЕБАННЫЙ НН СЛИТАЯ ХУЙНЯ! 5х5 Проебал, вантап гетнишь пмни {author.mention}")
    embed = discord.Embed(title=f'Вызвано {user}', color=user.color)
    embed.set_footer(text= f'Вызвано: {ctx.message.author}', icon_url= str(ctx.message.author.avatar_url))
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
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
@Bot.command(name = "стат")
async def num_msg(ctx, member: discord.Member = None):
    """Счетчик сообщний"""
    user = ctx.message.author if (member == None) else member
    number = await Messages(Bot).number_messages(user)
    embed = discord.Embed(description = f"Количество сообщений на сервере от **{user.name}** — **{number}**!")
    await ctx.send(embed = embed)
    
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

@Bot.command()
async def кнббан(ctx):
    author = ctx.message.author
    await ctx.send(f"{author.mention} ты **Выиграл**")

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

@Bot.command()
async def аватар(ctx, member : discord.Member = None):
    user = ctx.message.author if (member == None) else member
    await ctx.message.delete()
    embed = discord.Embed(title=f'Аватар пользователя {user}', description= f'[Ссылка на изображение]({user.avatar_url})', color=user.color)
    embed.set_footer(text= f'Вызвано: {ctx.message.author}', icon_url= str(ctx.message.author.avatar_url))
    embed.set_image(url=user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

#@Bot.command()
#async def игра(ctx, member: discord.Member = None):
#    await ctx.message.delete()
#    user = ctx.message.author if (member == None) else member
#    if user.activity: await ctx.send(f"Пользователь {user.mention} играет в **{user.activity}**")
#    else: await ctx.send(f"Пользователь {user.mention} ни во что не играет!")

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

@commands.command()
async def gw(self, ctx, seconds: int, *, text):
        '''простая команда создания розыгрыша-раздачи
        Время писать по схеме:   секунды, далее, произвольный текст приза'''
        def time_end_form(seconds):
            h = seconds // 3600
            m = (seconds - h * 3600) // 60
            s = seconds % 60
            if h < 10:
                h = f"0{h}"
            if m < 10:
                m = f"0{m}"
            if s < 10:
                s = f"0{s}"
            time_reward = f"{h} : {m} : {s}"
            return time_reward
        author = ctx.message.author
        time_end = time_end_form(seconds)
        message = await ctx.send(f"Розыгрыш!\nРазыгрывается:{text}\nЗавершится через {time_end}")
        await message.add_reaction("✔")
        while seconds > -1:
            time_end = time_end_form(seconds)
            text_message = f"Розыгрыш!\nРазыгрывается:{text}\nЗавершится через {time_end}"
            await message.edit(content=text_message)
            await asyncio.sleep(1)
            seconds -= 1
        channel = message.channel
        message_id = message.id
        message = await channel.fetch_message(message_id)
        reaction = message.reactions[0]
        users = await reaction.users().flatten()
        user = choice(users)
        await ctx.send(f'Ахтунг!\n Победитель розыгрыша - {user.mention}!\n '
                       f'Напишите {author.mention}, чтобы получить награду')

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
