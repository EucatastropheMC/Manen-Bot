# Import libraries
import discord

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

client.run('MTEzNDE4Nzc0ODAyMzA4MzE2MA.GUe0Sk.9uEQfzYsj1AhKFNX8zwx864Toj999_cBO10Kc0')
