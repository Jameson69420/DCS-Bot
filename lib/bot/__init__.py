from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed 
from discord.ext.commands import Bot as BotBase

PREFIX = ","
OWNER_IDS = [636894499515400213, 700189778817318934, 341047698255773696]


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

	def run(self, version):
		self.VERSION = version

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("runnning bot...")
		super().run(self.TOKEN, reconnect=True)   

	async def on_connect(self):
		print("bot online")

	async def on_disconnect(self):
		print("bot offline")

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(729852418988441672)
			print("bot ready")

			channel = self.get_channel(729852419869245502)
			await channel.send("Hello!")

			embed = Embed(title="Now online.", description="Welcome to Ducky Bot!", 
						  colour=0x6A3B8F, timestamp=datetime.utcnow())
			fields = [("Name", "DCS Bot", True),
					  ("Help", "Type ,help for help!", True),
					  ("Extra", "Make sure to type !rules in the bot command channel..", False)]
			for name, value, inline in fields: 		  
				embed.add_field(name=name, value=value, inline=inline)
			embed.set_author(name="DCS Bot", icon_url=self.guild.icon_url)
			embed.set_footer(text=" made by Jameson#0069")
			embed.set_thumbnail(url=self.guild.icon_url)
			await channel.send(embed=embed)

		else:
			print("bot reconnected")

	async def on_message(self, message):
		pass


bot = Bot()