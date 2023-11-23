from typing import Callable, TypeVar

from discord.ext import commands

from utils import dbmanager as db

T = TypeVar("T")


def can_execute(command: str, default: bool = False) -> Callable[[T], T]:
	"""
	This is a custom check to see if a user can execute a command.
	"""
	async def predicate(context: commands.Context) -> bool:
		if commands.is_owner(): # Owners bypass role checks
			return True
		allowed_roles: list = await db.list_roles(command)
		# Ensure the roles are sorted by position
		author_roles = list(sorted(context.author.roles, key=lambda role: role.position, reverse=True))
		for r1 in author_roles:
			for r2 in allowed_roles:
				if r1.id == r2[1]:
					return r2[2]
		# Role not found, return default value
		return default

	return commands.check(predicate)