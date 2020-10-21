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
from discord.ext import commands
from discord.ext.commands import Bot



prefix = '?'

Bot = commands.Bot(command_prefix= prefix)

Bot.remove_command('help')

@Bot.command(pass_context = True)
async def info(ctx):
    emb = discord.Embed(title= "Information about commands:globe_with_meridians:",colour= 0xfbfcfe)
    emb.add_field(name = "{}info".format(prefix), value= "**Show all commands**" )
    await ctx.send(embed= emb)
    emb = discord.Embed(title= "Game:video_game:", colour= 0x8B8989)
    emb.add_field(name = "{}rps".format(prefix), value= "**Play rock,paper,scissors with bots**")
    emb.add_field(name = "{}play".format(prefix), value= "**Heads and tails**", inline=False)
    await ctx.send(embed= emb)
    emb = discord.Embed(title= "Tools(Admin):tools:", colour= 0x8B8989)
    emb.add_field(name = "{}clear".format(prefix), value= "**Cleans chat from 1/10000**", inline=False)
    emb.add_field(name = "{}mute".format(prefix), value= "**Forbid the participant to write, speak**")
    emb.add_field(name = "{}unmute".format(prefix), value= "**Allow the participant to write, speak**")
    emb.add_field(name = "{}ban".format(prefix), value= "**Bans the participant**", inline=False)
    emb.add_field(name = "{}unban".format(prefix), value= "**Unbans the participant**", inline=False)	
    await ctx.send(embed= emb)
    emb = discord.Embed(title= "Buns", colour= 0x8B8989)
    emb.add_field(name = "{}avatar".format(prefix), value= "**Show the avatar of the specified member**", inline=False)
    emb.add_field(name = "{}userinfo".format(prefix), value= "**Shows all information about the user**", inline=False)
    emb.add_field(name = "{}wiki".format(prefix), value= "**Wikipedia**", inline=False)
    emb.set_footer(text= 'Owner channel https://www.youtube.com/channel/UCs5Eyo4mKVNXW1is7dU2pPA?(By Jutix)', icon_url='https://i.ibb.co/c3n8yNf/tumblr-f05f3d5c0e38233627b018bb9cff90a5-5ccccc19-400.gif')
    emb.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed= emb)
    

#------------------------------------------------------------------------------------------------------------------------#
@Bot.event
async def on_ready():
    print('I woke up after a stroke...')
    game = discord.Game(r"?info")
    await Bot.change_presence(status=discord.Status.online, activity=game)

#------------------------------------------------------------------------------------------------------------------------#

#@Bot.event
#async def on_member_join(member):
#    channel = Bot.get_channel(741329019198242897)
#    await channel.send(embed = discord.Embed(description = f'''📢User ``{member}`` joined📢''', color=0x009cd1))


#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
async def play(ctx):
    """Play with bot"""
    num=random.randint(1,2)
    if (num == 1):
           await ctx.send("You fell out :dollar: Eagle")
           print("[?coin] - done")
    if(num == 2):    
           await ctx.send("You fell out :yen: Tails")
           print("[?coin - done")
#------------------------------------------------------------------------------------------------------------------------#
@Bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 1000):
    """Clearing chat"""
    await ctx.message.delete() # I love Jutixxx
    await ctx.channel.purge(limit = amount) #deletes messages
    em = discord.Embed(description= f'it was remote *{amount}* messages', color = 708090) #settings embed
    await ctx.send(embed=em) #insert embed
    await asyncio.sleep(1) #wait timer
    await ctx.channel.purge(limit = 1) #Removes bot message
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
@Bot.command()
async def rps(ctx, move: str = None):
    solutions = ["`scissors`", "`rock`", "`paper`"]
    winner = "**DRAW**"
    p1 = solutions.index(f"`{move.lower()}`")
    p2 = randint(0, 2)
    if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0:
        winner = f"{ctx.message.author.mention} You **Lose**"
    elif p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1 or p1 == 0 and p2 == 2:
        winner = f"{ctx.message.author.mention} You **Won**"
    await ctx.send(    
        f"{ctx.message.author.mention} **=>** {solutions[p1]}\n"
        f"{Bot.user.mention} **=>** {solutions[p2]}\n"
        f"{winner}")

        

#------------------------------------------------------------------------------------------------------------------------# 
    
@Bot.command()
async def avatar(ctx, member : discord.Member = None):
    user = ctx.message.author if (member == None) else member
    await ctx.message.delete()
    embed = discord.Embed(title=f'User avatar {user}', description= f'[Image link]({user.avatar_url})', color=user.color)
    embed.set_footer(text= f'Caused by: {ctx.message.author}', icon_url= str(ctx.message.author.avatar_url))
    embed.set_image(url=user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

#------------------------------------------------------------------------------------------------------------------------#

import wikipedia
@Bot.command()
async def wiki(ctx, *, args):
  try:
    wikipedia.set_lang("en")
    new_page = wikipedia.page(f'{args}')
    summ = wikipedia.summary(f'{args}', sentences=5)
    emb = discord.Embed(title=new_page.title,
                        description=f"{summ}",
                        color=0xEE82EE)
    emb.add_field(name="For a full review of the article, follow the link:", value=f"[Reference]({new_page.url})")
    await ctx.send(embed=emb)
  except Exception:
    return await ctx.send('Ambiguous argument, specify the article', delete_after=5)

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
async def userinfo(ctx, Member: discord.Member = None, member : discord.Member = None):
    await ctx.message.delete()
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='User info'.format(Member.name), description=f"Logged into the server: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
    f"Main nickname: {Member.name}\n\n"
    
   f"Custom nickname: {Member.nick}\n\n"
                                                                                      f"ID: {Member.id}\n\n"
                                                                                      f"Main role: {Member.top_role}\n\n"
                                                                                      f"Discord with: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color= 0xEE82EE, timestamp=ctx.message.created_at)

    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Создано: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

#------------------------------------------------------------------------------------------------------------------------#

# _____                _       #
#|_   _|              | |      #
#  | |    ___    ___  | | ___  #
#  | |   / _ \  / _ \ | |/ __| #
#  | |  | (_) || (_) || |\__ \ #
#  \_/   \___/  \___/ |_||___/ #
#							   #



#------------------------------------------------------------------------------------------------------------------------#

@Bot.command(pass_context= True)
async def Hi(ctx):
    await ctx.send("Hi my friend! {}".format(ctx.message.author))

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick ( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    await member.kick( reason = reason )
    await ctx.send( f'User has been kicked! { member.mention }' )


#------------------------------------------------------------------------------------------------------------------------#

@Bot.command()
async def ban(ctx, member:discord.Member, seconds:int):
  await ctx.send(f'User {member.name} got banned on {seconds} seconds')
  await member.ban()
  await asyncio.sleep(seconds)
  await member.unban()

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def mute ( ctx, member: discord.Member, *, reason = None ):
    await ctx.chanell.purge( limit = 1 )

    await member.mute( reason = reason )
    await ctx.send(f'Пользователь {member.name} получил мут на {seconds} секунд')

#------------------------------------------------------------------------------------------------------------------------#

@Bot.command( pass_context = True )

async def unban( ctx, *, member ):
    await ctx.channel.purge( limit = 1 )

    banned_useres = await ctx.guild.band()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban( user )
        await ctx.send( f'The user was unbanned! { user.mention }')

        return

#------------------------------------------------------------------------------------------------------------------------#


import discord
import random
import io
import sys
from discord.ext import commands
import asyncio
import datetime

class Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild.id == 698510531538976799: # Сюда ид своего сервера
            return    
        if not message.author.bot:
            channel = self.bot.get_channel(768578202821591050) # Сюда ид текстового канала
            embed = discord.Embed(
                description = 'Сообщения было удалено', 
                colour = 0x2f3136,
                timestamp = datetime.datetime.utcnow())
            for a in message.attachments:
                if a.filename.endswith((".png", ".jpg", ".gif", ".mp4")):
                    embed.set_image(url = f'{a.proxy_url}')
                    break
            embed.add_field(name = 'Удалённое сообщение: ', value = f'```{message.content}```' or f'{a.proxy_url}', inline = False)
            embed.add_field(name = 'Автор сообщения: ', value = f'{message.author.mention}', inline = True)
            embed.add_field(name = 'В канале: ', value = f'{message.channel.mention}')
            embed.set_footer(text = f'ID сообщения: {message.id}')
            await channel.send(embed = embed)

    @commands.Cog.listener() 
    async def on_message_edit(self, before, after):
        if not before.guild.id == 698510531538976799: # Сюда ид своего сервера
            return            
        if not before.author.bot:
            if before.author != self.bot.user:
                channel = self.bot.get_channel(768578202821591050) # Сюда ид текстового канала
                embed = discord.Embed(
                    description = 'Сообщение было отредактировано', 
                    colour = 0x2f3136,
                    timestamp = datetime.datetime.utcnow())
                embed.add_field(name = 'Старое содержимое:', value = f'```{before.content}```', inline = False)
                embed.add_field(name = 'Новое содержимое:', value = f'```{after.content}```', inline = False)
                embed.add_field(name = 'Автор', value = before.author.mention)
                embed.add_field(name = 'Канал', value = before.channel.mention)
                embed.set_footer(text = f'ID сообщения: {before.id}')
                await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.guild.id == 698510531538976799: # Сюда ид своего сервера
            return
        if not member.bot:
            channel_id = self.bot.get_channel(768578202821591050) # Сюда ид текстового канала
            embed = discord.Embed(
                description = f'Участник **{member.name}** {member.mention} присоединился к серверу',
                color = 0x8af889,
                timestamp = datetime.datetime.utcnow())
            embed.set_footer(text = f"Зарегистрированный {member.created_at}"[:45])
            await channel_id.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.guild.id == 698510531538976799: # Сюда ид своего сервера
            return
        if not member.bot:
            channel_id = self.bot.get_channel(768578202821591050)
            embed = discord.Embed(
                description = f'Участник **{member.name}** {member.mention} покинул сервер',
                color = 0xffff00,
                timestamp = datetime.datetime.utcnow())
            embed.set_footer(text = f"Зарегистрированный {member.created_at}"[:45])
            await channel_id.send(embed = embed)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.guild.id == 698510531538976799: # Сюда ид своего сервера
            return

        if not len(before.roles) == len(after.roles):
            role = [ ]
            if len(before.roles) > len(after.roles):
                for i in before.roles:
                    if not i in after.roles:
                        role.append(f'Убраны роли {i.name}(<@&{i.id}>)\n')
            elif len(before.roles) < len(after.roles):
                for i in after.roles:
                    if not i in before.roles:
                        role.append(f'Добавлены роли {i.name}(<@&{i.id}>)\n')
            
            str_a = ''.join(role)
            channel = self.bot.get_channel(768578202821591050) # Сюда ид текстового канала
            embed = discord.Embed(
                description = f'Роли участника **{before.display_name}** {after.mention} были изменены',
                color = 0x2f3136,
                timestamp = datetime.datetime.utcnow())
            embed.add_field(name = f'{str_a[:14]}', value = f"**{str_a[14:]}**", inline = False)
            embed.set_footer(text = f'ID сообщения: {before.id}')
            return await channel.send(embed = embed)

        if not before.display_name == after.display_name:
            channel = self.bot.get_channel(768578202821591050) # Сюда ид текстового канала
            embed = discord.Embed(
                description = f'Никнейм участника **{before.display_name}** {after.mention} были изменен',
                color = 0x2f3136,
                timestamp = datetime.datetime.utcnow())
            embed.add_field(name = 'Старый никнейм:', value = f'{before.display_name}', inline = False)
            embed.add_field(name = 'Новый никнейм:', value = f'{after.display_name}', inline = False)
            embed.set_footer(text = f'ID сообщения: {before.id}')
            await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before = None, after = None):
        if not member.guild.id == 698510531538976799: # Сюда ид своего сервера
            return
        if after.channel == None:
            if not before.channel == None:
                if member.bot:
                    return
                channel = self.bot.get_channel(768578202821591050) # Сюда ид текстового канала
                embed = discord.Embed(
                    description = f'Участник **{member.display_name}** {member.mention} вышел из голосового канала',
                    color = 0x2f3136,
                    timestamp = datetime.datetime.utcnow())
                embed.add_field(name = 'Покинул', value = f'**{before.channel.name}** {before.channel.mention}')
                return await channel.send(embed = embed)

        if (not before.channel == None) and (not after.channel == None):
            if before.channel.id == after.channel.id:
                return

            if member.bot:
                return
            channel = self.bot.get_channel(768578202821591050) # Сюда ид текстового канала
            embed = discord.Embed(
                description = f'Участник **{member.display_name}** {member.mention} перешёл в другой голосового канала',
                color = 0x2f3136,
                timestamp = datetime.datetime.utcnow())
            embed.add_field(name = 'Присоединился:', value = f'**{after.channel.name}** {after.channel.mention}', inline = False)
            embed.add_field(name = 'Покинул:', value = f'**{before.channel.name}** {before.channel.mention}', inline = False)
            return await channel.send(embed = embed)

        if not after.channel == None:
            if before.channel == None:
                if member.bot:
                    return
                channel = self.bot.get_channel(768578202821591050) # Сюда ид текстового канала
                embed = discord.Embed(
                    description = f'Участник **{member.display_name}** {member.mention} подключился к голосовому каналу',
                    color = 0x2f3136,
                    timestamp = datetime.datetime.utcnow())
                embed.add_field(name = 'Присоединился:', value = f'**{after.channel.name}** {after.channel.mention}')
                return await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
    	await ctx.message.delete()

    	if isinstance(error, commands.CommandNotFound):
    		return
    	embed = discord.Embed(
    		title = 'Ошибка',
    		description = f'Отказано в доступе!',
    		color = 0x2f3136)
    	embed.set_thumbnail(url = f'{ctx.author.avatar_url}')
    	await ctx.send(embed = embed, delete_after = 15)

#------------------------------------------------------------------------------------------------------------------------#


token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
