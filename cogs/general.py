import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		name = "help",
		description = "List all commands the bot has loaded"
	)
	async def help_cmd(self, context: Context) -> None:
		embed = discord.Embed(
			title="mcbot", description="List of available commands:", color=0x9C84EF
		)
		for i in self.bot.cogs:
			cog = self.bot.get_cog(i.lower())
			commands = cog.get_commands()
			data = []
			for command in commands:
				description = command.description.partition("\n")[0]
				data.append(f"{command.name} - {description}")
			help_text = "\n".join(data)
			embed.add_field(
				name = i.capitalize(),
				value = f"```{help_text}```",
				inline = False
			)
		await context.send(embed=embed)

	@commands.hybrid_command(
		name = "info",
		description = "Show information about the bot"
	)
	async def info_cmd(self, context: Context) -> None:
		embed = discord.Embed(
			title="mcbot", description="Version 0.2.0", color=0x9C84EF
		)
		await context.send(embed=embed)


async def setup(bot):
	await bot.add_cog(General(bot))