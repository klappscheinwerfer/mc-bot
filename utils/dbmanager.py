import aiosqlite
import os

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"
SCHEMA_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/schema.sql"


async def init_db():
	# TODO: check if database already exists
	async with aiosqlite.connect(DATABASE_PATH) as db:
		with open(SCHEMA_PATH) as file:
			await db.executescript(file.read())
		await db.commit()


async def set_setting(key, value):
	pass

async def get_setting(key):
	pass
