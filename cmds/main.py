import discord
from discord.ext import commands
from core.classes import Cog_Extension
import time
from datetime import datetime

class Main(Cog_Extension):
	
	@commands.command(name='ping', help='機器人延遲')
	async def ping(self, ctx):
		t1 = time.perf_counter()
		await ctx.trigger_typing()
		t2 = time.perf_counter()
		await ctx.trigger_typing()
		nowtime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		embed=discord.Embed(title="延遲(PING)", color=ctx.author.colour)        
		embed.add_field(name="機器人延遲", value=f"```{round(self.bot.latency*1000)} ms```", inline=True)
		embed.add_field(name="系統延遲", value=f"```{round((t2-t1)*1000)} ms```", inline=True)
		embed.set_footer(text=f"bot {nowtime}")
		await ctx.send(embed=embed)



def setup(bot):
	bot.add_cog(Main(bot))
