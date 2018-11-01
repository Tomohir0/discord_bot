import discord
from discord.ext import commands
import pprint
import os
import pickle
import random

#import boto3
#bucket_name = "tomo-discord"
#s3 = boto3.resource('s3')
## s3連携


class Note():
    "メモについての関数があるよ！みんなでメモを保存したり晒したりしよう！"

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

    @commands.command(description='「?notes」で保存されたmemoからランダムに一つを晒します。', pass_context=True)
    async def callrand(self, ctx: commands.Context):
        "「?callrand」でメモを1つ晒します。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
        else:
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
            label_selected = random.choice(list(memos.keys()))
            await self.bot.say(label_selected +" : "+ memos.get(label_selected, "ERROR"))

    @commands.command(description='「?notes」で保存されたmemoを読み出すことができます。', pass_context=True)
    async def deletes(self, ctx: commands.Context, label: str):
        "「?delete secret」でsecretとして保存されたメモを削除できる……かも。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
        else:
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
            if not label in memos:
                await self.bot.say(label + "なんてラベルないよ！「?labels」使う？")
            elif random.randint(1, 100) > 90:
                await self.bot.say(label+"の「"+memos.pop(label)+"」は消えちゃった……")
            else:
                await self.bot.say(label + "の「" + memos.get(label) + "」は消えちゃった……")
                await self.bot.say("\nと思いきや復活！！神！")
                await self.bot.say(label + " : " + memos.get(label))

def setup(bot):
    bot.add_cog(Note(bot))
