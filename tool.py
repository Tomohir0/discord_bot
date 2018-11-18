import discord
from discord.ext import commands
import pprint
import random
import os
import qrcode
import pickle

#import boto3
#bucket_name = "tomo-discord"
#s3 = boto3.resource('s3')
## s3連携


class Tool():
    "サイコロとかランダム選択とか、かゆいところに手が届くツールとなる関数だよ！要望があれば何でも言ってみて！"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="",pass_context=True)
    async def qr(self, ctx, *text: str):
        "渡されたテキストからQRコードを生成するよ！プログラミングらしさあるけど、sourceは十行もないよ！"
        img = qrcode.make(" ".join(text))
        img.save("/tmp/img_tmp.png")
        await self.bot.send_file(ctx.message.channel, "/tmp/img_tmp.png")

    @commands.command(pass_context=True)
    async def qr_calls(self, ctx, label: str):
        "「?calls」と連携してmemoの内容からQRcodeを作成します。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
            return 0
        with open(f_name, 'rb') as f:
            memos = pickle.load(f) 
        text = memos.get(label, label + "なんてlabelのメモないよ！")
        img = qrcode.make(text)
        img.save("/tmp/img_tmp.png")
        await self.bot.send_file(ctx.message.channel, "/tmp/img_tmp.png")

    @commands.command(pass_context=True)
    async def qr_sel_calls(self, ctx):
        "「?sel_calls」と連携してmemoの内容からQRcodeを作成します。"
        ctx.message.context = "?sel_calls"
        await self.bot.process_commands(ctx.message)
        text = ctx.message.content
        img = qrcode.make(text)
        img.save("/tmp/img_tmp.png")
        await self.bot.send_file(ctx.message.channel, "/tmp/img_tmp.png")

    @commands.command(description='「?roll 2d6」で「3, 5」などが得られます。')
    async def roll(self,dice: str):
        """サイコロを振ることができます。TRPGで使われるNdN記法。2個の6面サイコロの結果がほしい場合は「?roll 2d6」と入力してください。"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say("「NdN」の形じゃないよ！")
            return 0

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say("ダイスロール！\n" + result)

    @commands.command(description='「?choice A B C」などのように入力してください。')
    async def choose(self,*choices: str):
        """選択肢からランダムに一つ選びます。「?choose」の後に選択肢をスペースで区切って入力してください。"""
        if random.randint(1, 3) > 1:
            await self.bot.say(random.choice(choices) + "にするしかないじゃない！")
        else:
            await self.bot.say("ﾀﾞﾗﾗﾗﾗﾗﾗﾗﾗﾗ～\nダン！！\n見事選ばれたのは" + random.choice(choices) + "でした！！")

    @commands.command(description="「?cite qr」で直前の内容をQRcodeに！", pass_context=True)
    async def cite(self,ctx,*,command: str):
        "直前のmessageを引数としてcommandを実行できちゃう！"
        m = ""
        count = 0
        async for msg in self.bot.logs_from(ctx.message.channel, limit=2):
            count += 1
            if count == 1:
                continue
            m = msg.content + "\n"
        ctx.message.content = "?" + command +" "+ m
        await self.bot.process_commands(ctx.message)

    @commands.command(description="", pass_context=True)
    async def cites(self, ctx, number_of_messages: int,*, command: str):
        "直前の複数のmessageを引数としてcommandを実行できちゃう！"
        m = ""
        count = 0
        async for msg in self.bot.logs_from(ctx.message.channel, limit=number_of_messages + 1):
            count += 1  # command文は含まない
            if count == 1:
                continue
            m = msg.content + "\n" + m # 順序を考慮して前につけていくべき
        ctx.message.content = "?" + command +" "+ m
        await self.bot.process_commands(ctx.message)

    @commands.command(description="", pass_context=True)
    async def cites_auth(self, ctx, number_of_messages: int, *, command: str):
        "直前の複数のmessageをauthor名付きで引数としてcommandを実行できちゃう！"
        m = ""
        count = 0
        async for msg in self.bot.logs_from(ctx.message.channel, limit=number_of_messages + 1):
            count += 1  # command文は含まない
            if count == 1:
                continue
            m = msg.author.name + " : " + msg.content + "\n" + m  # 順序を考慮して前につけていくべき
        ctx.message.content = "?" + command + " " + m
        await self.bot.process_commands(ctx.message)

    @commands.command(description="指定した件数分のbotのmessageを消去します。削除できる件数が少なくなることもあるかもしれません。", pass_context=True)
    async def clean_m(self, ctx, number_of_messages: int):
        "ついついたまりがちなbotのmessageを適度にオソウジ！くるくる！"
        delete_count = 0
        async for msg in self.bot.logs_from(ctx.message.channel, limit=1000):
            if msg.author == self.bot.user:
                if delete_count >= number_of_messages:
                    break
                await self.bot.delete_message(msg)
                delete_count += 1
        await self.bot.say("完了！")                


def setup(bot):
    bot.add_cog(Tool(bot))
