import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import os
import bot
from discord import client, guild, member
from random import randint, choice
import threading
import time









Bot = commands.Bot(command_prefix= "!")

@Bot.event
async def on_ready():
    print('online!')
    game = discord.Game(r"Vanila Майнкрафт")
    await Bot.change_presence(status=discord.Status.online, activity=game)

@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(698660443291385906)
    role = discord.utils.get(member.guild.roles, id= 698514876313894993)
    await member.add_roles(role)
    await channel.send(embed = discord.Embed(description = f'''📢Пользователь ``{member}`` 
    присоеденился📢''', color=0x0c0c0c))

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
async def гадиклох(ctx):
    author = ctx.message.author
    await ctx.send(f"Полностью согласен с вашем мнением!:white_check_mark: {author.mention}")

@Bot.command()
@commands.has_permissions(administrator = True)
async def say(ctx, *args):
    await ctx.message.delete()
    args = ' '.join(args).split('/', maxsplit = 1)
    try:
        user = Bot.get_user(int(args[0][args[0].find("!") + 1 : -1]))
        await user.send(args[1])
    except:
        await ctx.send(args[0])

@Bot.command()
async def спор(ctx):
    num=random.randint(1,2)
    if (num == 1):
           await ctx.send("Вым выпал :dollar: Орёл")
           print("[?coin] - done")
    if(num == 2):    
           await ctx.send("Вам выпала :yen: Решка")
           print("[?coin - done")

@Bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def очистить(ctx, amount = 100):
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

@Bot.command(name = "msg")
async def num_msg(ctx, member: discord.Member = None):
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

#bans a user with a reason
@Bot.command()
@commands.has_any_role("Keyblade Master","Foretellers")
async def ban (ctx, member:discord.User=None, reason =None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("Ты не можешь забанить самого себя")
        return
    if reason == None:
        reason = "Вел себя плохо!"
    message = f"Ты был забанен на {ctx.guild.name} потому-что {reason}"
    await member.send(message)
    # await ctx.guild.ban(member, reason=reason)
    await ctx.channel.send(f"{member} был забанен")

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
