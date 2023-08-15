import discord
from discord.ext import commands

bot = commands.Bot()


@bot.slash_command(name="createfile", guild_ids=[1105196644808527872])
async def createfile(ctx):
    await ctx.respond("Command executed successfully.")

bot.run('MTEzNDE4Nzc0ODAyMzA4MzE2MA.GUe0Sk.9uEQfzYsj1AhKFNX8zwx864Toj999_cBO10Kc0')
