import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from utils import dbmanager as db


class Owner(commands.Cog, name="owner"):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		name="sync",
		description="Synchonize the slash commands"
	)
	@app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
	@commands.is_owner()
	async def sync_cmd(self, context: Context, scope: str) -> None:
		if scope == "global":
			await context.bot.tree.sync()
			embed = discord.Embed(
				description="Slash commands have been globally synchronized",
				color=discord.Color.from_str(await db.get_setting("embed-color")),
			)
			await context.send(embed=embed)
			return
		elif scope == "guild":
			context.bot.tree.copy_global_to(guild=context.guild)
			await context.bot.tree.sync(guild=context.guild)
			embed = discord.Embed(
				description="Slash commands have been synchronized in this guild",
				color=discord.Color.from_str(await db.get_setting("embed-color")),
			)
			await context.send(embed=embed)
			return
		embed = discord.Embed(
			description="The scope must be `global` or `guild`",
			color=discord.Color.from_str(await db.get_setting("embed-error-color"))
		)
		await context.send(embed=embed)

	@commands.hybrid_command(
		name="unsync",
		description="Unsynchonize the slash commands",
	)
	@app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
	@commands.is_owner()
	async def unsync_cmd(self, context: Context, scope: str) -> None:
		if scope == "global":
			context.bot.tree.clear_commands(guild=None)
			await context.bot.tree.sync()
			embed = discord.Embed(
				description="Slash commands have been globally unsynchronized",
				color=discord.Color.from_str(await db.get_setting("embed-color")),
			)
			await context.send(embed=embed)
			return
		elif scope == "guild":
			context.bot.tree.clear_commands(guild=context.guild)
			await context.bot.tree.sync(guild=context.guild)
			embed = discord.Embed(
				description="Slash commands have been unsynchronized in this guild",
				color=discord.Color.from_str(await db.get_setting("embed-color")),
			)
			await context.send(embed=embed)
			return
		embed = discord.Embed(
			description="The scope must be `global` or `guild`",
			color=discord.Color.from_str(await db.get_setting("embed-error-color"))
		)
		await context.send(embed=embed)

	@commands.hybrid_command(
		name="set",
		description="Change a setting",
	)
	@app_commands.describe(key="Key", value="Value")
	@commands.is_owner()
	async def set_cmd(self, context: Context, key: str, value: str) -> None:
		await db.set_setting(key, value)
		embed = discord.Embed(
			description=f"{key}:{value}",
			color=discord.Color.from_str(await db.get_setting("embed-color")),
		)
		await context.send(embed=embed)

	@commands.hybrid_command(
		name="list",
		description="List all settings",
	)
	@commands.is_owner()
	async def list_cmd(self, context: Context) -> None:
		embed = discord.Embed(
			title="mcbot",
			description="List of all settings:",
			color=discord.Color.from_str(await db.get_setting("embed-color")),
		)
		for i in await db.list_settings():
			embed.add_field(
				name = i[0],
				value = i[1],
				inline = False
			)
		await context.send(embed=embed)

async def setup(bot):
	await bot.add_cog(Owner(bot))