from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed 
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from ..db import db

PREFIX = ","
OWNER_IDS = [636894499515400213, 700189778817318934, 341047698255773696]


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		db.autosave(self.scheduler)
		super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

	def run(self, version):
		self.VERSION = version

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("runnning bot...")
		super().run(self.TOKEN, reconnect=True)

	async def print_message(self):
	   channel = self.get_channel(729852419869245502)
	   await channel.send("Bot Uptime Test.")

	async def rules_reminder(self):
	   await self.stdout.send("Weekly reminder to check the rules!")

	async def on_connect(self):
		print("bot online")

	async def on_disconnect(self):
		print("bot offline")

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Something went wrong...")

		await self.stdout.send("An error occurred...")
		raise

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass

		elif hasattr(exc, "original"):
			raise exc.original

		else:
			raise exc

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(729852418988441672)
			self.stdout = self.get_channel(729852419869245502)
			self.scheduler.add_job(self.print_message, CronTrigger(minute="30"))
			self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
			self.scheduler.start()

			await self.stdout.send("Hello!")

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

			print("bot ready")

		else:
			print("bot reconnected")

	async def on_message(self, message):
		pass


bot = Bot()