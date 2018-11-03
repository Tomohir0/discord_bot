import discord
from discord.ext import commands
import pprint
import random
import os
import pickle

import numpy as np

#import boto3
#bucket_name = "tomo-discord"
#s3 = boto3.resource('s3')
# s3連携



class Game():
    " "

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='', pass_context=True)
    async def king(self, ctx: commands.Context):
        "王様ゲームをdiscordで再現……できるかな？まずは「?king」"
        await self.bot.say("王様ゲームを始めたいなら「!start」、止めたいなら「!stop」を入力してね")

        for role in [role for role in ctx.message.server.roles if role.name in ["ゲーム参加者", "王様"]]:
            try:
                await self.bot.delete_role(ctx.message.server, role)
            except:
                pass
        role_join = await self.bot.create_role(ctx.message.server, name="ゲーム参加者", hoist=True, position=0)
        role_king = await self.bot.create_role(ctx.message.server, name="王様", hoist=True, position=1)

        def check_st(msg):
            return msg.content in ["!start", "!stop"]

        start_or_stop = await self.bot.wait_for_message(check=check_st)

        if start_or_stop.content == "!stop":
            await self.bot.say("終了！お疲れ様！")
            try:
                for role in [role for role in ctx.message.server.roles if role.name in ["ゲーム参加者", "王様"]]:
                    await self.bot.delete_role(ctx.message.server, role)
            finally:
                return 0

        await self.bot.say("王様ゲームを始めよう！\n参加希望者は「!join」\n抜けたくなったら「!esc」"
                           "\n全員の入力が完了したら「!start」\nゲームを終了したい場合は「!stop」")

        def check_join(msg):  # join checkのお時間
            return msg.content in ["!join", "!esc", "!start", "!stop"]
        
        while(True): # !stopで抜ける
            not_start = True
            while (not_start): # join
                join_or = await self.bot.wait_for_message(check=check_join)
                await self.bot.say(join_or.author.display_name + "、了解")
                if join_or.content == "!stop":
                    await self.bot.say("終了！お疲れ様！")
                    for role in [role for role in ctx.message.server.roles if role.name in ["ゲーム参加者", "王様"]]:
                        await self.bot.delete_role(ctx.message.server, role)
                    return 0
                if join_or.content == "!join":
                    await self.bot.add_roles(join_or.author, role_join)
                if join_or.content == "!esc":
                    await self.bot.remove_roles(join_or.author, role_join)
                if join_or.content == "!start":
                    await self.bot.say("参加者締め切り！役職の「ゲーム参加者」を確認してね！")
                    not_start = False
            
            join_list = [member for member in ctx.message.server.members if role_join in member.roles]
            join_num = len(join_list)
            if join_num < 3:
                await self.bot.say("あ～、少なすぎ……かな？またの機会ということで！")
                await self.bot.say("終了！お疲れ様！")
                for role in [role for role in ctx.message.server.roles if role.name in ["ゲーム参加者", "王様"]]:
                    await self.bot.delete_role(ctx.message.server, role)
                return 0

            await self.bot.say("今回の参加者は" + str(join_num) + "人！\nさて、はじめよう(何か入力してね)")
            await self.bot.wait_for_message()
            await self.bot.say("王様だ～れだ！")
            king = random.choice(join_list)
            await self.bot.say(king.display_name + "！！"
                            "\nさあ、王様！ 1~" + str(join_num - 1) + "の数字を使ってご命令を！"
                            "\n(命令を言い終えたら王自身が「!do」とご入力を！)")

            def check_do(msg):
                return msg.startswith == "!do" and msg.author == king
            await self.bot.wait_for_message(check=check_do)
            await self.bot.say("では番号の発表です！(ここだけ仕様が少し変……)")

            join_list.remove(king)  # 王様を省く
            join_pairs = zip(join_list.shuffle(), list(
                range(join_num-1)))  # 数字とのペアを生成
            m = ""
            for member, number in join_pairs:
                m += number + " : " + member.display_name + "\n"
            await self.bot.say(m)

            await self.bot.say("命令の実行をご確認されるなどして、次に進むべきとご判断なされたならば王様自身が「!next」とご入力を！")

            def check_next(msg):
                return msg.startswith == "!next" and msg.author == king
            await self.bot.wait_for_message(check=check_next)
            await self.bot.say("これで今回の王様ゲームは終わり！")
            await self.bot.remove_roles(king, role_king)

            await self.bot.say("抜けたくなった人は「!esc」を入力してね。新たな参加希望者は「!join」を入力。"
                            "\n全員の入力が完了したら「!start」を入力。ゲームを終了したい場合は「!stop」を。")
            

    @commands.command(description='', pass_context=True)
    async def number_game(self, ctx: commands.Context):
        "数当てゲーム！範囲は1~100だよ！"
        await self.bot.say("数当てゲームのお時間です。1~100の中にある正解を当てよう！チャンスは全部で約7回！")
        def check_num(msg):
           return 0 < msg.content
        answer = random.randint(1, 100)
        var = random.randint(0, 3)

        for i in range(6+var):
            await self.bot.say(str(i+1)+"回目、いくつだと思う～？") # dictでバリエーション増やしたい
            try_num = await self.bot.wait_for_message(check=check_num)
            await self.bot.say("さてさて……")
            err = try_num.content - answer

            find_table = {np.arange(-100,- 30) : "小さすぎるんじゃない？",
                          np.arange(-29,-20) : "まだ小さい小さい",
                          np.arange(-19,-10) : "うんうん、まだ小さい",
                          np.arange(-9,-5) : "ま、まあまあいいと思うよ？もう少し増やせるんじゃない？？",
                          np.arange(-4,-2) : "げ",
                          np.arange(-1,1) : "うげら",
                          np.arange(2,4) : "げ",
                        np.arange(5,9) : "えーっと……まだ減らせる、かな……",
                        np.arange(10,19) : "うんうん、減らしてこ",
                        np.arange(20,29) : "まだ大きいよー！",
                        np.arange(30,100) : "大きすぎるんじゃない？"}
            if err == 0:
                break
            for key in find_table.keys():
                if err in list(key):
                    await self.bot.say(find_table.get(key))
                    break
        if err == 0:
            await self.bot.say("お見事！")
            return 0
        await self.bot.say("残念……。正解は" + str(answer) + "でした！")

    @commands.command(pass_context=True)
    async def dobon(self, ctx):
        "ドボンゲーム(準備中)"


def setup(bot):
    bot.add_cog(Game(bot))
