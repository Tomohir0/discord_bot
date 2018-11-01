import discord
from discord.ext import commands
import pprint
import os
import pickle

##import boto3
#bucket_name = "tomo-discord"
#s3 = boto3.resource('s3')
## s3連携

class Note():

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(description='serverのみんなでmemoを共有できます。', pass_context=True)
    async def notes(self, ctx: commands.Context, label: str, *, memo: str):
        "「?notes secret ギルマスは実は高校生」とすれば、secretラベルで「ギルマスは実は高校生」を記録できます。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            memos = {}
        else:
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
        memos[label] = memo
        with open(f_name, 'wb') as f:
            pickle.dump(memos, f)  # 古いリストに付け足す形で
        await self.bot.say("覚えました！！")

    @commands.command(description='「?notes」で保存されたmemoを読み出すことができます。', pass_context=True)
    async def calls(self, ctx: commands.Context, label: str):
        "「?calls secret」でsecretとして保存されたメモを読み出します。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
        else:
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
                await self.bot.say(memos.get(label, label + "なんてlabelのメモないよ！"))

    @commands.command(description=' ', pass_context=True,)
    async def labels(self, ctx: commands.Context):
        "「?notes」のlabelの一覧を表示します。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
        else:
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
                await self.bot.say("ここのmemoのlabel一覧は\n")
                for label in memos.keys():
                    await self.bot.say(label)
                await self.bot.say("\nだよ！")
def setup(bot):
    bot.add_cog(Note(bot))