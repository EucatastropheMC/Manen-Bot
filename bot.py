import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guild = discord.Object(id=1105196644808527872)


@tree.command(name="createfile", description="Create or update a character file", guild=guild)
async def create_file(interaction):
    await interaction.response.send_message("Hello!")


@client.event
async def on_ready():
    await tree.sync(guild=guild)
    print("Commands synchronized.")
