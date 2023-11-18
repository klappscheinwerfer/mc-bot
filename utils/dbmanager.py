import aiosqlite
import os

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"
SCHEMA_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/schema.sql"
DEFAULT_VALUES_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/default.sql"


async def init_db() -> None:
	if os.path.exists(DATABASE_PATH):
		# Database already exists, return
		print("Found database")
		return
	async with aiosqlite.connect(DATABASE_PATH) as db:
		# Create schema
		with open(SCHEMA_PATH) as file:
			await db.executescript(file.read())
		# Insert default values
		with open(DEFAULT_VALUES_PATH) as file:
			await db.executescript(file.read())
		await db.commit()
		print("Created database")
	return


async def set_setting(key, value) -> None:
	async with aiosqlite.connect(DATABASE_PATH) as db:
		# Check if setting already exists
		async with db.execute(
			"SELECT * FROM setting WHERE setting_key=?",
			(key,)
		) as cursor:
			if await cursor.fetchone() == None:
				# Setting does not exit, insert new
				await db.execute(
					"INSERT INTO setting(setting_key, setting_value) VALUES (?, ?)",
					(key, value,)
				)
			else:
				# Setting already exists, update
				await db.execute(
					"UPDATE setting SET setting_value=? WHERE setting_key=?",
					(value, key,)
				)
		await db.commit()
		return
	

async def get_setting(key) -> str:
	async with aiosqlite.connect(DATABASE_PATH) as db:
		rows = await db.execute(
			"SELECT * FROM setting WHERE setting_key=?",
			(key,)
		)
		return (await rows.fetchone())[1]


async def list_settings() -> list:
	async with aiosqlite.connect(DATABASE_PATH) as db:
		async with db.execute(
			"SELECT setting_key, setting_value FROM setting"
		) as cursor:
			result = await cursor.fetchall()
			return result
