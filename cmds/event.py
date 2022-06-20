import discord
from discord.ext import commands
from core.classes import Cog_Extension, Gloable_Data
from core.errors import Errors
import json
import datetime
import asyncio

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Event(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''指令錯誤觸發事件'''
        Gloable_Data.errors_counter += 1
        error_command = '{0}_error'.format(ctx.command)
        if hasattr(Errors, error_command):  # 檢查是否有 Custom Error Handler
            error_cmd = getattr(Errors, error_command)
            await error_cmd(self, ctx, error)
            return
        else:  # 使用 Default Error Handler
            await Errors.default_error(self, ctx, error)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} join {member.guild.name}!')
        guild = member.guild.name
        if guild == "軟軟的FBK":
            channel = self.bot.get_channel(int("811225288389951538"))
            embed = discord.Embed(title=f"歡迎{member}進入fbk香香的尾巴", description="0w0",
                                  color=0x1fb32d, timestamp=datetime.datetime.now(datetime.timezone.utc))
            embed.set_thumbnail(url=f"{member.avatar_url}")

            embed.add_field(
                name="伺服器人數：", value=f"{member.guild.member_count}", inline=True)
            embed.add_field(name=member, value="請先看看公告喔")
            embed.set_footer(text="FBK專用bot")
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Event(bot))
