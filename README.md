# mc-bot

A Discord bot for interacting with a Minecraft server.

## Installation

* Update `apt-get update`
* Install python, virtualenv and git `apt install python3 virtualenv python3-virtualenv git`
* Clone the repository and move to it `git clone https://github.com/klappscheinwerfer/mc-bot`
* Copy the config file and edit it `cp config.example.json config.json`
* Create the virtual environment `virtualenv -p python3 ./venv`
* Activate the virtual environment `source venv/bin/activate`
	* Deactivate with `deactivate`
* Install requirements `pip install -r requirements.txt`
* Run `python bot.py`

## Notes

* The bot needs permission for sending messages and slash commands
* If you're running the bot for the first time, sync slash commands (see config.json)
* The server start script should check if the server is already launched