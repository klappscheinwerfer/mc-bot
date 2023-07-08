import asyncio
import discord
import os
import subprocess

from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv
from mcstatus import JavaServer


class Minecraft(commands.Cog, name="minecraft"):
	def __init__(self, bot):
		self.bot = bot

		load_dotenv()
		self.address = os.getenv("ADDRESS")
		self.port = int(os.getenv("PORT"))
		self.inactive_time = 0
		self.time_limit = int(os.getenv("INACTIVE_TIME_LIMIT"))
		self.server = JavaServer(self.address, self.port)
		self.start_server_path = os.getenv("START_SERVER_PATH")
		self.stop_server_path = os.getenv("STOP_SERVER_PATH")

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
					subprocess.call(self.stop_server_path)
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

	"""
	@commands.hybrid_command(
		name="status",
		description="Check if the server is online",
	)
	async def status(self, context: Context):
		pass
	"""

	@commands.hybrid_command(
		name="start",
		description="Starts the server",
	)
	async def start(self, context: Context):
		try:
			lat = await asyncio.wait_for(self.server.async_ping(), timeout=5)
			embed = discord.Embed(
				title="mcbot", description="Server is already online", color=0x9C84EF
			)
		except (asyncio.TimeoutError, ConnectionRefusedError):
			# Server is not reachable - can be started
			try:
				subprocess.call(self.start_server_path)
				embed = discord.Embed(
					title="mcbot", description="Server started", color=0x9C84EF
				)
			except Exception as e:
				embed = discord.Embed(
					title="mcbot", description=f"Server start failed: {e}", color=0x9C84EF
				)
		await context.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Minecraft(bot))