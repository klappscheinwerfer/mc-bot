import asyncio
import discord
import os
import subprocess

from discord.ext import commands, tasks
from discord.ext.commands import Context
from mcstatus import JavaServer

from utils import checks


class Minecraft(commands.Cog, name="minecraft"):
	def __init__(self, bot):
		self.bot = bot
		self.inactive_time = 0
		self.time_limit = self.bot.config["inactive_time_limit"]
		self.server = JavaServer(self.bot.config["address"], self.bot.config["port"])

	@commands.Cog.listener()
	async def on_ready(self):
		self.check_task.start()

	@tasks.loop(minutes=1.0)
	async def check_task(self):
		try:
			status = await asyncio.wait_for(self.server.async_status(), timeout=5)
			if status.players.online == 0:
				# No players online
				if self.inactive_time > self.time_limit:
					# Turn server off
					print("Time limit exceeded, turning server off")
					subprocess.call(self.bot.config["stop_server_path"])
					self.inactive_time = 0
				else:
					self.inactive_time += 1
			else:
				# Players online => reset timer
				self.inactive_time = 0
		except (asyncio.TimeoutError, ConnectionRefusedError):
			# Server is not reachable
			if self.inactive_time != 0:
				self.inactive_time = 0

	@commands.hybrid_command(
		name="status",
		description="Check if the server is online",
	)
	@checks.can_execute(command="status", default=True)
	async def status_cmd(self, context: Context):
		await context.interaction.response.defer()
		if(await self.status_check()):
			await context.interaction.followup.send("Server is online")
		else:
			await context.interaction.followup.send("Server is offline")

	@commands.hybrid_command(
		name="start",
		description="Start the server",
	)
	@checks.can_execute(command="start", default=True)
	async def start_cmd(self, context: Context):
		await context.interaction.response.defer()
		if(await self.status_check()):
			await context.send("Server is already online")
		else:
			# Server is not reachable - can be started
			try:
				subprocess.call(self.bot.config["start_server_path"])
				await context.interaction.followup.send("Server started")
			except Exception as e:
				await context.interaction.followup.send(f"Server start failed: {e}")

	async def status_check(self):
		try:
			latency = await asyncio.wait_for(self.server.async_ping(), timeout=5)
			return True
		except (asyncio.TimeoutError, ConnectionRefusedError):
			return False
		except Exception as e:
			print(f"Exception: {e}")
			return False

async def setup(bot):
	await bot.add_cog(Minecraft(bot))