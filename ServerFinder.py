import discord
from discord.ext import commands
import socket
import json

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='.', intents=intents)

# Lista de servidores de Minecraft
servers = [
    {"name": "Gold Server", "address": "gold.magmanode.com", "port": 28706},
    {"name": "Another Server", "address": "another.server.com", "port": 25565}
]

# Función para hacer el ping al servidor
def check_server_status(address, port):
    packet = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    try:
        # Establecer el socket para TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        # Conectar al servidor
        sock.connect((address, port))

        # Enviar paquete para obtener la respuesta del servidor
        sock.sendall(packet)

        # Recibir la respuesta
        data = sock.recv(1024)

        # Extraer la información del paquete recibido
        response = data[3:]  # El primer byte es el tamaño de la respuesta
        response_data = json.loads(response.decode('utf-8'))

        # Obtener el estado del servidor
        status = f"Status: Online\n"
        status += f"Players: {response_data['players']['online']}/{response_data['players']['max']}\n"
        status += f"Version: {response_data['version']['name']}\n"
        
        sock.close()
        return status
    except Exception as e:
        return f"Status: Offline\nError: {str(e)}"

# Comando para encontrar servidores
@bot.command()
async def findserver(ctx):
    response = "Finded Servers:\n"
    for server in servers:
        status = check_server_status(server['address'], server['port'])
        response += f"\n{server['name']}: {server['address']}:{server['port']}\n{status}"
    await ctx.send(response)

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

# Ejecutar el bot
bot.run('MTM2MzczMTQ3NzQ1NTU3MzA5Mw.GRdvg5.eevMZIV_-fChz0gGqn2Znl37H-RLvne9AAS9yU')
