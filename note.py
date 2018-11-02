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
'''
global
'''
del_try_count = 0

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
            return 0
        with open(f_name, 'rb') as f:
            memos = pickle.load(f)
        await self.bot.say(memos.get(label, label + "なんてlabelのメモないよ！"))

    @commands.command(description=' ', pass_context=True,)
    async def labels(self, ctx: commands.Context):
        "「?notes」のlabelの一覧を表示します。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
            return 0
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
            return 0
        with open(f_name, 'rb') as f:
            memos = pickle.load(f)
        label_selected = random.choice(list(memos.keys()))
        await self.bot.say(label_selected +" : "+ memos.get(label_selected, "ERROR"))

    @commands.command(description='「?notes」で保存されたmemoを削除することができるかもしれません。', pass_context=True)
    async def dels(self, ctx: commands.Context, label: str):
        "「?dels secret」でsecretとして保存されたメモを削除できる……かも。"
        global del_try_count
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
            return 0
        with open(f_name, 'rb') as f:
                memos = pickle.load(f)
        if not label in memos:
            await self.bot.say(label + "なんてラベルないよ！「?labels」使う？")
            return 0
        if del_try_count > 3:
            await self.bot.say("残念！もう回数制限だね！時間をあけて再チャレンジ！")
            return 0
        if random.randint(1, 100) > 40:
            await self.bot.say(label+" : "+memos.pop(label)+"\nは消えちゃった……")
            return 0
        await self.bot.say(label + " : " + memos.get(label) + "\nは消えちゃった……")
        await self.bot.say("\nと思いきや復活！！神！")
        await self.bot.say(label + " : " + memos.get(label))

    @commands.group(description=' ', pass_context=True,)
    async def selects(self, ctx: commands.Context):
        "「?notes」のlabelの一覧を見ながらlabelを選択して内容を表示します。"
        if ctx.invoked_subcommand is None:
            f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
            if not os.path.isfile(f_name):  # 存在しないときの処理
                await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
                return 0
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
            await self.bot.say("ここのmemoの一覧は\n")
            for label in memos.keys():
                await self.bot.say(label+" : " + memos.get(label)[:10])
            await self.bot.say("\nさあ、どれを見る？label名を入力してね！")

    @call_select.command()
    async def quit(ctx: commands.Context, label: str)
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        with open(f_name, 'rb') as f:
            memos = pickle.load(f)
        await self.bot.say(memos.get(label,"ないよ！"))




def setup(bot):
    bot.add_cog(Note(bot))
