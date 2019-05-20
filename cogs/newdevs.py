import discord
from datetime import datetime
import pytz
from utils.role import cargos
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from discord.ext import commands
from asyncio import sleep
import requests
from pymongo import MongoClient
import pymongo

class newDevs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(570906068277002271)
        channel = discord.utils.get(guild.channels, id=571029261448773688)

        if channel is None:
            return
        if not payload.channel_id == 571029261448773688:
            return
        if payload.channel_id == None:
            return
        
        if payload.user_id in self.cooldown:
            return

        for cargo in cargos:
            if cargo['emoji'] == str(payload.emoji):
                guild = self.bot.get_guild(payload.guild_id)
                cargo = guild.get_role(cargo['id'])
                membro = guild.get_member(payload.user_id)
                if cargo not in membro.roles:
                    await membro.add_roles(cargo)
                    self.cooldown.append(payload.user_id)
                    self.cooldown.remove(payload.user_id)
                break
                
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        channel = discord.utils.get(guild.channels, id=571029261448773688)
        if not payload.channel_id == 571029261448773688:
            return
        if payload.user_id in self.cooldown:
            return

        for cargo in cargos:
            if cargo['emoji'] == str(payload.emoji):
                guild = self.bot.get_guild(payload.guild_id)
                cargo = guild.get_role(cargo['id'])
                membro = guild.get_member(payload.user_id)
                if cargo in membro.roles:
                    await membro.remove_roles(cargo)
                    self.cooldown.append(payload.user_id)
                    self.cooldown.remove(payload.user_id)
                break

    @commands.Cog.listener()  
    async def on_member_remove(self, member):
       if member.guild.id == 570906068277002271:
        canal = discord.utils.get(member.guild.channels, id=570908352000032798)
        membros = len(member.guild.members)
        texto = "<:newDevs:573629564627058709> | **Membros** : "+str(membros).replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣")
        await canal.edit(topic=texto)
    
    @commands.Cog.listener()  
    async def on_member_join(self, member):
       if member.guild.id == 570906068277002271:
        url = requests.get(member.avatar_url_as(format="png"))
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((245, 245));
        bigsize = (avatar.size[0] * 2,  avatar.size[1] * 2)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        saida = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        saida.putalpha(mask)
        saida.save('cogs/img/avatar.png')

        fundo = Image.open('cogs/img/bemvindo.png')
        fonte = ImageFont.truetype('cogs/img/arial.ttf',42)
        fonte2 = ImageFont.truetype('cogs/img/arial.ttf',58)

        escrever = ImageDraw.Draw(fundo)
        escrever.text(xy=(365,215), text=str(member.name),fill=(255,255,255),font=fonte)
        escrever.text(xy=(405,283), text=str(member.discriminator),fill=(255,255,255),font=fonte2)
        escrever.text(xy=(365,372), text="New Dev's",fill=(255,255,255),font=fonte)

        fundo.paste(avatar, (52, 133), avatar)
        fundo.save("cogs/img/welcome.png")   
        canal = discord.utils.get(member.guild.channels, id=570908348204187668)
        await canal.send(f"Olá {member.mention}, seja bem vindo ao **New Dev's**, caso queria algum **CARGO** use o <#571029261448773688> para pegar, e leia as <#571018188540739588> para ficar por dentro do servidor.", file=discord.File('cogs/img/welcome.png'))
        
        canal = discord.utils.get(member.guild.channels, id=570908352000032798)
        membros = len(member.guild.members)
        texto = "<:newDevs:573629564627058709> | **Membros** : "+str(membros).replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣")
        await canal.edit(topic=texto)
        '''
        json ={
             "E0":"<:numero0:580090018505162755>",
             "E1":"<:numero1:580088324946133015>",
             "E2":"<:numero2:580088325101191198>",
             "E3":"<:numero3:580088325595987968>",
             "E4":"<:numero4:580088324782424078>",
             "E5":"<:numero5:580088325004853268>",
             "E6":"<:numero6:580088324971167774>",
             "E7":"<:numero7:580088325054922772>",
             "E8":"<:numero8:580088325000527942>",
             "E9":"<:numero9:580088325491261453>"
             }
        text = str(len(member.guild.members))
        for n in range(0, 10):
            text = text.replace(str(n), "E"+str(n))
        for n in range(0, 10):
            text = text.replace("E"+str(n), json["E"+str(n)])                                                  
        texto = "<:newDevs:573629564627058709> **| Membros** : {}".format(text)
        await canal.edit(topic=texto)
        '''
  
def setup(bot):
    bot.add_cog(newDevs(bot))
