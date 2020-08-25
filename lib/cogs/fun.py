from discord.ext.commands import Cog


class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot

		@Cog.listener
		async def on_ready(self):
			self.bot.stdout.send("Fun Cog loaded!")

def setup(bot):
	bot.add_cog(Fun(bot))