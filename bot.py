import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random

Bot = commands.Bot(command_prefix= "!")


 #@Bot.event
 #async def on_member_join(member):
    # role = discord.utils.get(member.server.roles, name="Мороженко")
   #  await add_roles(member, role)

@Bot.event
async def on_ready():
    print('online!')
    game = discord.Game(r"Vanila Майнкрафт")
    await Bot.change_presence(status=discord.Status.online, activity=game)

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







           
Bot.run("Njk4MjgxNDU1MTU0ODg4ODg0.XpDu1Q.hX1dSRBcH89Os_vhY-kK4Gc_b6k")