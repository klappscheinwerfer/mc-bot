from typing import Callable, TypeVar

from discord.ext import commands

from utils import dbmanager as db

T = TypeVar("T")


def can_execute(command: str, default: bool = False) -> Callable[[T], T]:
	"""
	This is a custom check to see if a user can execute a command.
	"""
	async def predicate(context: commands.Context) -> bool:
		allowed_roles: list = await db.list_allowed_roles(command)
		author_roles = context.author.roles
		for r1 in allowed_roles:
			for r2 in author_roles:
				if r1 == r2: return True
		# Role not found, return default value
		return default

	return commands.check(predicate)