import asyncio
import discord
import json
import os
import sys

from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from utils import dbmanager

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
	sys.exit("'config.json' not found")
else:
	with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
		config = json.load(file)

intents = discord.Intents.default()

bot = Bot (
	command_prefix="",
	intents=intents,
	help_command=None,
	owner_ids = config["owners"]
)

# Config variable
bot.config = config


@bot.event
async def on_ready() -> None:
	if bot.config["sync_commands_globally"]:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} command(s)")
	print("Ready!")


async def load_cogs() -> None:
	for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
		if file.endswith(".py"):
			extension = file[:-3]
			try:
				print(f"Loaded cogs.{extension}")
				await bot.load_extension(f"cogs.{extension}")
			except Exception as e:
				print(e)


asyncio.run(dbmanager.init_db())
asyncio.run(load_cogs())
bot.run(bot.config["token"])