import discord
from discord.ext import commands
import pprint
import random
import os
import qrcode
import pickle

import matplotlib
import matplotlib.pyplot as 

#import boto3
#bucket_name = "tomo-discord"
#s3 = boto3.resource('s3')
## s3連携


class Plot():
    "サイコロとかランダム選択とか、かゆいところに手が届くツールとなる関数だよ！要望があれば何でも言ってみて！"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="", pass_context=True)
    async def qr(self, ctx, *text: str):
        "渡されたテキストからQRコードを生成するよ！プログラミングらしさあるけど、sourceは十行もないよ！"
        img = qrcode.make(" ".join(text))
        img.save("/tmp/img_tmp.png")
        await self.bot.send_file(ctx.message.channel, "/tmp/img_tmp.png")




def setup(bot):
    bot.add_cog(Plot(bot))
