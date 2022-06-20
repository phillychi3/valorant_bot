import discord
from discord.ext import commands
from core.classes import Cog_Extension
import requests
import json
from core.getdata import *
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


class val(Cog_Extension):

    @commands.command()
    async def matched(self, ctx):
        with open('players.json', 'r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        if str(ctx.author.id) not in jdata:
            await ctx.send('您尚未註冊，請使用addplayer')
            return
        await ctx.send(file=discord.File(fp=battle_generate_image(get_placer_battle_info("phillychi3","4353","ap")), filename='r6players.png'))
        


    @commands.command()
    async def addplayer(self, ctx, player):
        data = player.split("#")
        name = data[0]
        tag = data[1]
        data = requests.get(
            f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}", headers=header).json()
        if data["status"] != 200:
            await ctx.send("not find player")
            return
        data = data["data"]
        region = data["region"]
        with open("./players.json", "r", encoding="utf-8") as f:
            players = json.load(f)

        try:
            test = players[str(ctx.author.id)]["tag"]
            if name != players[str(ctx.author.id)]["name"] or tag != players[str(ctx.author.id)]["tag"]:
                players[ctx.author.id] = {
                    "name": name,
                    "tag": tag,
                    "region": region
                }
                with open("./players.json", "w", encoding="utf-8") as f:
                    json.dump(players, f, indent=4)
                await ctx.send(f"{name}#{tag} 已更新資料庫")
                return
        except:
            players[ctx.author.id] = {
                "name": name,
                "tag": tag,
                "region": region
            }
            with open("./players.json", "w", encoding="utf-8") as f:
                json.dump(players, f, indent=4)

        await ctx.send(f"{name}#{tag} 已加入資料庫")


def setup(bot):
    bot.add_cog(val(bot))
