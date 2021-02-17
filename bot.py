import discord
from discord.ext import commands
import requests
import os 


array = []

with open("output.txt","r") as f:
    for line in f.readlines():
        array.append(line.split(' '))

#You have to create a output.txt to write on

bot = commands.Bot(command_prefix='.')
client = discord.Client()
token ="YOURTOKEN"
server="YOURIPSERVER"
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Bot on")

@bot.command()
async def hola(ctx):
    await ctx.send(f'.Hola {ctx.author.name}')

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Help",color=discord.Color.blue())
    embed.add_field(name=".hola", value="Devuelve un hola a quien me escriba.", inline=False)
    embed.add_field(name=".server", value="Te dice si el server esta encendido , su versión y su ip.", inline=False)
    embed.add_field(name=".players", value="Te dice que jugadores están conectados.", inline=False)
    embed.add_field(name=".location", value="Te muestra las localizaciones guardadas", inline=False)
    embed.add_field(name=".locationadd", value="Para añadir localizaciones se añade con Nombre.Coordenadas .", inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def server(ctx):
    response = requests.get('https://api.mcsrvstat.us/2/'+server)
    if (response.json()["online"] == (True)):
      
        await ctx.send(f"``` Servidor encendido \n Version : " + response.json()["version"] + " \n Ip: "+response.json()["ip"]+ ":"+ str(response.json()["port"]) + " ``` ")
    else:
        await ctx.send(f"Servidor apagado :C")  

@bot.command()
async def players(ctx): 
    response = requests.get('https://api.mcsrvstat.us/2/'+server)
    if (response.json()["online"] == (True)):
      if(response.json()["players"]["online"]>0):
        print(response.json()["players"]["list"])
        await ctx.send(response.json()["players"]["list"])
      else:
        await ctx.send(f"No hay nadie conectado")  
    else:
        await ctx.send(f"Servidor apagado :C ")  

@bot.command()
async def locationadd(ctx, arg ): 
    x="\n"+ arg
    array.append(x.split("."))
    print(array)
    with open("output.txt", "w") as f:
        for line in array:
            f.writelines(" ".join(line))
    await ctx.send(f"Localizacion añadida")
@bot.command()
async def location(ctx):
    salida=""
    for i in array:
      salida+=(i[0] +" ``"+ i[1]+ "``")
    await ctx.send(salida)
    
bot.run(token)
