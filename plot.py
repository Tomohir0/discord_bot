import discord
from discord.ext import commands
import pprint
import random
import os
# import qrcode
import pickle

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import urllib.request

#import boto3
#bucket_name = "tomo-discord"
#s3 = boto3.resource('s3')
## s3連携


class Plot():
    "いろいろPlotするよ！"

    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="", pass_context=True)
    async def plot_hist(self, ctx, url: str):
        "dat fileをdlしてhistgramを生成します。"
        title = "/tmp/date_tmp.dat"
        urllib.request.urlretrieve(url, "{0}".format(title))
        dat = pd.read_table(title)
        
        label = []
        label[0] = dat[0][0] # python 正規表現扱い習得
        label[1] = dat[0][1]

        dat = dat[[label[0],label[1]]].dropna()

        fig = plt.figure()

        ax = fig.add_subplot(111)
        #ax.set_xlim([-10, 10])
        #ax.set_ylim([-10, 10])
        H = ax.hist2d(dat[label[0]], dat[label[1]], bins=100)

        ax.set_xlabel(label[0])
        ax.set_ylabel(label[1])
        fig.colorbar(H[3], ax=ax)
        plt.show()
        plt.savefig('/tmp/img_tmp.png')
        await self.bot.send_file(ctx.message.channel, "/tmp/img_tmp.png")


def setup(bot):
    bot.add_cog(Plot(bot))
