import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


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
				color=0x9C84EF,
			)
			await context.send(embed=embed)
			return
		elif scope == "guild":
			context.bot.tree.copy_global_to(guild=context.guild)
			await context.bot.tree.sync(guild=context.guild)
			embed = discord.Embed(
				description="Slash commands have been synchronized in this guild",
				color=0x9C84EF,
			)
			await context.send(embed=embed)
			return
		embed = discord.Embed(
			description="The scope must be `global` or `guild`", color=0xE02B2B
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
				color=0x9C84EF,
			)
			await context.send(embed=embed)
			return
		elif scope == "guild":
			context.bot.tree.clear_commands(guild=context.guild)
			await context.bot.tree.sync(guild=context.guild)
			embed = discord.Embed(
				description="Slash commands have been unsynchronized in this guild",
				color=0x9C84EF,
			)
			await context.send(embed=embed)
			return
		embed = discord.Embed(
			description="The scope must be `global` or `guild`", color=0xE02B2B
		)
		await context.send(embed=embed)

async def setup(bot):
	await bot.add_cog(Owner(bot))