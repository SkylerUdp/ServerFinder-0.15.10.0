import discord
from discord.ext import commands
from mcstatus import MinecraftServer


intents = discord.Intents.default()
bot = commands.Bot(command_prefix='.', intents=intents)


servers = [
    {"name": "Gold Server", "address": "gold.magmanode.com", "port": 28706},
    {"name": "Another Server", "address": "another.server.com", "port": 25565}
]


def check_server_status(address, port):
    try:
        server = MinecraftServer(address, port)
        status = server.status()
        return f"Status: Online\nPlayers: {status.players.online}/{status.players.max}"
    except:
        return "Status: Offline"


@bot.command()
async def findserver(ctx):
    response = "Finded Servers:\n"
    for server in servers:
        status = check_server_status(server['address'], server['port'])
        response += f"\n{server['name']}: {server['address']}:{server['port']}\n{status}"
    await ctx.send(response)


@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')


bot.run('TU_BOT_TOKEN')
