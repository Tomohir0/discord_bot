import discord
from discord.ext import commands
import pprint
import random
#import os
#import pickle

#import boto3
#bucket_name = "tomo-discord"
#s3 = boto3.resource('s3')
## s3連携


class Tool():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='「?roll 2d6」で「3, 5」などが得られます。')
    async def roll(dice: str):
        """サイコロを振ることができます。TRPGで使われるNdN記法。2個の6面サイコロの結果がほしい場合は「?roll 2d6」と入力してください。"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say("「NdN」の形じゃないよ！")
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say("ダイスロール！\n" + result)


    @commands.command(description='「?choice A B C」などのように入力してください。')
    async def choose(*choices: str):
        """選択肢からランダムに一つ選びます。「?choose」の後に選択肢をスペースで区切って入力してください。"""
        if random.randint(1, 3) > 1:
            await self.bot.say(random.choice(choices) + "にするしかないじゃない！")
        else:
            await self.bot.say("ﾀﾞﾗﾗﾗﾗﾗﾗﾗﾗﾗ～\nダン！！\n見事選ばれたのは" + random.choice(choices) + "でした！！")


def setup(bot):
    self.bot.add_cog(Tool(bot))
