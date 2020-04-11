import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import os
import bot
from discord import client
from random import randint, choice










Bot = commands.Bot(command_prefix= "!")

#@Bot.event
#async def on_member_join(ctx):
#    await ctx.send("Приветствуем тебя на сервере Пломбир 2.0 {server} {user}!")

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
    args = ''.join(args).split('/', maxsplit = 1)
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
    await asyncio.sleep(3) #таймер ожидания
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

ID_COLOR_ROLE = 657246845290020885
ID_SERVER = 526870790864502794
class Hueta(commands.Cog):

    def __init__(self, bot):
        self.colors = 0xFF0000, 0xFF7F00, 0xFFFF00, 0x00FF00, 0x0000FF, 0x4B0082, 0x9400D3
        self.bot = bot
        self.color_role = None
    
    @commands.command(name='pidor', aliases=['пидор', 'пидарас', 'ЛГБТ'])
    async def cmd_lgbt(self, ctx, member:discord.Member=None):
        member = ctx.author if member is None else member

        if self.color_role in member.roles:
            return await ctx.send(f"Пользователь {member.mention} уже итак {choice(['пидор', 'пидарас', 'педарасина'])}")

        embed = discord.Embed(description=f"{member.mention} Теперь ты {choice(['пидор', 'пидарас', 'педарасина'])}!", colour=0xffffff)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Вызвал(a): {ctx.author.nick if ctx.author.nick else ctx.author.name}', icon_url=ctx.author.avatar_url)

        await member.add_roles(self.color_role)
        return await ctx.send(embed=embed)

    async def __loop_edit_color_role(self):
        while not self.bot.is_closed():
            try:
                await self.color_role.edit(colour=discord.Colour(choice(self.colors)))
                await asyncio.sleep(15)
            except Exception:
                break

    @commands.Cog.listener()
    async def on_ready(self):
        self.color_role = self.bot.get_guild(ID_SERVER).get_role(ID_COLOR_ROLE)
        self.bot.loop.create_task(self.__loop_edit_color_role())

def setup(bot):
    bot.add_cog(Hueta(bot))

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
