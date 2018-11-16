import discord
from discord.ext import commands
import pprint
import os
import pickle
import random
import asyncio
import sys

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
        
    @commands.command(description='serverのみんなでmemoを共有できます。standard', pass_context=True)
    async def notes(self, ctx: commands.Context, label: str, *,memo: str):
        "「?notes secret ギルマスは実は高校生」とすれば、secretラベルで「ギルマスは実は高校生」を記録できます。label名に重複があれば確認が出ます。"
        # memo = " ".join(memo)  #list => str
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            memos = {}
        else:
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
            
        if label in memos.keys():
            def check_auth(msg):
                return msg.author == ctx.message.author
            await self.bot.say("すでに" + label + "というmemoは存在します。"
                               "\n上書きするなら「w」、後ろに付け足すなら「a」、前に付け足すなら「f」、labelを変更するなら「<そのlabel名>」を、キャンセルするなら「c」を入力してください。")
            select = await self.bot.wait_for_message(check=check_auth)
        else:
            select = ctx.message # messageははじめから用意ておかないとだめ
            select.content = "w" # 被りがないなら実質上書き
        
        if select.content == "w":
            memos[label] = memo
        elif select.content == "a":
            memos[label] = memos[label] + "\n" + memo
        elif select.content == "f":
            memos[label] = memo + "\n" + memos[label] 
        elif select.content == "c":
            await self.bot.say("おけおけ、また改めて！")
            return 0
        else: # label変更
            memos[select.content] = memo
        with open(f_name, 'wb') as f:
            pickle.dump(memos, f)  # 古いリストに付け足す形で
        await self.bot.say("覚えました！！")

    @commands.command(description='serverのみんなでmemoを共有できます。overwite', pass_context=True)
    async def notew(self, ctx: commands.Context, label: str, *, memo: str):
        "重複があっても上書きしかする気がない人のための「?note」"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            memos = {}
        else:
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
        memos[label] = memo
        with open(f_name, 'wb') as f:
            pickle.dump(memos, f)  # 古いdictに付け足す形で
        await self.bot.say("覚えました！！")

    @commands.command(description='serverのみんなでmemoを共有できます。add', pass_context=True)
    async def notea(self, ctx: commands.Context, label: str, *, memo: str):
        "重複があったら付け足ししかする気がない人のための「?note」"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            memos = {}
        else:
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
        memos[label] = memos[label] +"\n" + memo
        with open(f_name, 'wb') as f:
            pickle.dump(memos, f)  # 古いdictに付け足す形で
        await self.bot.say("覚えました！！")

    @commands.command(description='serverのみんなでmemoを共有できます。forward', pass_context=True)
    async def notef(self, ctx: commands.Context, label: str, *, memo: str):
        "重複があったら「前に」付け足ししかする気がない人のための「?note」"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            memos = {}
        else:
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
        memos[label] =  memo +"\n" +memos[label] 
        with open(f_name, 'wb') as f:
            pickle.dump(memos, f)  # 古いdictに付け足す形で
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
        ctx.message.content = memos.get(label)

    @commands.command(description=' ', pass_context=True,)
    async def labels(self, ctx: commands.Context):
        "「?notes」のlabelの一覧を表示します。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
            return 0
        with open(f_name, 'rb') as f:
            memos = pickle.load(f)
        await self.bot.say("ここのmemoのlabel一覧は")
        m=""
        for label in memos.keys():
            m += label + "\n"
        await self.bot.say(m+"だよ！")

    @commands.command(description='callrand。「?notes」で保存されたmemoからランダムに一つを晒します。', pass_context=True)
    async def callr(self, ctx: commands.Context):
        "「?callrand」でメモを1つ晒します。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
            return 0
        with open(f_name, 'rb') as f:
            memos = pickle.load(f)
        label_selected = random.choice(list(memos.keys()))
        await self.bot.say(label_selected +" : "+ memos.get(label_selected, "ERROR"))

    @commands.group(description='「?notes」で保存されたmemoを削除することができるかもしれません。「sudo」版もあります', pass_context=True)
    async def dels(self, ctx: commands.Context, label: str):
        "「?dels secret」でsecretとして保存されたメモを削除できる………かも。"
        if ctx.invoked_subcommand is None:
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
                await self.bot.say(label + " : " + memos.pop(label) + "\nは消えちゃった……")
                with open(f_name, 'wb') as f:
                    pickle.dump(memos,f)
                return 0
            await self.bot.say(label + " : " + memos.get(label) + "\nは消えちゃった……")
            await self.bot.say("\nと思いきや復活！！神！")
            await self.bot.say(label + " : " + memos.get(label))


    @dels.command(description='sudo関数です。使用できる人は限られています。', pass_context=True,sudo="sudo")
    async def sudo_dels(self, ctx: commands.Context, label: str):
        "sudo関数です。labelで指定したメモを確実に削除できます。使用できる人は限られています。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if ctx.message.author.id != "349102495114592258":
            await self.bot.say("You are not authorized for sudo function, baby")
            return 0
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
            return 0
        with open(f_name, 'rb') as f:
                memos = pickle.load(f)
        if not label in memos:
            await self.bot.say(label + "なんてラベルないよ！「?labels」使う？")
            return 0
        await self.bot.say(label+" : "+memos.pop(label)[:5]+"\nは消えちゃった……")

    @commands.command(description='select_calls', pass_context=True)
    async def sel_c(self, ctx: commands.Context):
        "「?notes」のlabelの一覧を見ながらlabelを選択して内容を表示します。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
            return 0
        with open(f_name, 'rb') as f:
            memos = pickle.load(f)
        await self.bot.say("ここのmemoの一覧は")
        m=""
        for label in memos.keys():
            m+= label+" : " + memos.get(label)[:5]+"\n"
        await self.bot.say(m+"さあ、どれを見る？label名を入力してね！")
        def check(msg):
            return msg.content in memos.keys() and msg.author == ctx.message.author # check関数
        label_input = await self.bot.wait_for_message(check = check) # label入力
        ctx.message.content = "?calls " + label_input.content
        await self.bot.process_commands(ctx.message)  # calls起動
        
    @commands.group(description='select_dels', pass_context=True)
    async def sel_d(self, ctx: commands.Context):
        "labelの一覧を見ながらメモを選択して消去できるかもしれません。"
        if ctx.invoked_subcommand is None:
            f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
            if not os.path.isfile(f_name):  # 存在しないときの処理
                await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
                return 0
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
            await self.bot.say("ここのmemoの一覧は")
            m=""
            for label in memos.keys():
                m+=label+" : " + memos.get(label)[:5]+"\n"
            await self.bot.say(m+"さあ、どれを消す？label名を入力してね！")

            def check(msg):
                return msg.content in memos.keys() and msg.author == ctx.message.author # check関数
            label_input = await self.bot.wait_for_message(check=check)  # label入力
            ctx.message.content = "?dels " + label_input.content
            await self.bot.process_commands(ctx.message)  # dels起動

    @sel_d.command(description='sudo_select_dels', pass_context=True,sudo="sudo")
    async def sudo_sel_d(self, ctx: commands.Context):
        "labelの一覧を見ながらメモを選択して確実に消去できます。sudo関数です。使用できる人は限られています。"
        f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
        if not os.path.isfile(f_name):  # 存在しないときの処理
            await self.bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
            return 0
        with open(f_name, 'rb') as f:
            memos = pickle.load(f)
        await self.bot.say("ここのmemoの一覧は")
        for label in memos.keys():
            await self.bot.say(label+" : " + memos.get(label)[:5])
        await self.bot.say("さあ、どれを消す？label名を入力してね！")

        def check(msg):
            return msg.content in memos.keys() and msg.author == ctx.message.author  # check関数
        label_input = await self.bot.wait_for_message(check=check)  # label入力
        ctx.message.content = "?dels " + label_input.content + " sudo"
        await self.bot.process_commands(ctx.message)  # sudo_dels起動

def setup(bot):
    bot.add_cog(Note(bot))
