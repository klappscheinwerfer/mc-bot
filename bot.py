import asyncio
import discord
import os
import sys

from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

bot = Bot (
	command_prefix="",
	intents=intents,
	help_command=None
)


@bot.event
async def on_ready() -> None:
	#synced = await bot.tree.sync()
	#print(f"Synced {len(synced)} command(s)")
	print("Ready!")


async def load_cogs() -> None:
	for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
		if file.endswith(".py"):
			extension = file[:-3]
			try:
				await bot.load_extension(f"cogs.{extension}")
			except Exception as e:
				print(e)


asyncio.run(load_cogs())
bot.run(TOKEN)