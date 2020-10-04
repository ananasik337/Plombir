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
    emb.add_field(name = "{}аватар".format(prefix), value= "**Показ автарки указанного участника**", inline=False)
    emb.add_field(name = "{}userinfo".format(prefix), value= "**Показывает всю информацию о пользователе!**", inline=False)
    emb.add_field(name = "{}wiki".format(prefix), value= "**Википедия**", inline=False)
    emb.set_footer(text= 'сайт автора jutix.xyz опечатано 2020 ©', icon_url='https://i.ibb.co/0n03k4G/ava.png')
    emb.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed= emb)
    

#------------------------------------------------------------------------------------------------------------------------#
@Bot.event
async def on_ready():
    print('Очнулся после инсульта...')
    game = discord.Game(r"!инфо")
    await Bot.change_presence(status=discord.Status.online, activity=game)

#------------------------------------------------------------------------------------------------------------------------#

@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(741329019198242897)
    await channel.send(embed = discord.Embed(description = f'''📢Пользователь ``{member}`` присоеденился📢''', color=0x009cd1))

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
@commands.has_permissions(administrator= True)
async def mute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name= "Muted")
    await member.add_roles(mute_role)
    author = ctx.message.author
    await ctx.send(f"Человек был успешно замучен!:white_check_mark: {author.mention}")

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
@commands.has_permissions(administrator= True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name= "Muted")
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

import wikipedia
@Bot.command()
async def wiki(ctx, *, args):
  try:
    wikipedia.set_lang("ru")
    new_page = wikipedia.page(f'{args}')
    summ = wikipedia.summary(f'{args}', sentences=5)
    emb = discord.Embed(title=new_page.title,
                        description=f"{summ}",
                        color=0xEE82EE)
    emb.add_field(name="Для полного ознакомления со статьей, перейдите по ссылке:", value=f"[Ссылочка]({new_page.url})")
    await ctx.send(embed=emb)
  except Exception:
    return await ctx.send('Неоднозначный аргумент, уточните статью', delete_after=5)

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
async def стас(ctx, member : discord.Member):
    await ctx.send(f"{ctx.author.mention} https://i.ibb.co/1QYjpKJ/image0.jpg", "Молодец, ты нашел пасхалку!")

#------------------------------------------------------------------------------------------------------------------------#
@Bot.command()
async def userinfo(ctx, Member: discord.Member = None, member : discord.Member = None):
    await ctx.message.delete()
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о юзере'.format(Member.name), description=f"Зашел на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
    f"Основной никнаме: {Member.name}\n\n"
    
   f"Кастомный никнейм: {Member.nick}\n\n"
                                                                                      f"Айди: {Member.id}\n\n"
                                                                                      f"Основная роль: {Member.top_role}\n\n"
                                                                                      f"В дискорде с: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color= 0xEE82EE, timestamp=ctx.message.created_at)

    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Создано: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)
#------------------------------------------------------------------------------------------------------------------------#


token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
