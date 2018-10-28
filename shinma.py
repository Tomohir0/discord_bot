import discord
import datetime
import pprint
import random
from discord.ext import commands

description = ('''神魔管理のために作られたbotです。挨拶をしたり愛をささやいたりもします。
\n「神魔登録説明」で神魔登録などについての説明を表示します。\nその他のcommandについては「?help」を確認してください。「?」を文頭に置いて適宜使用できます。''')
bot = commands.Bot(command_prefix='?', description=description)
date_register = "2000-01-01"
shinma1 = ""
shinma2 = ""
note = ""
# async外で保存するためにGlobal変数を用いる


@bot.event  # server加入時の処理
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):  # 関数名はon_messageのみ
    date_today = datetime.date.today()
    global date_register, shinma1, shinma2  # Global宣言
    mc = message.content
    if bot.user != message.author:  # botによるbotの反応を避ける   
        # ぼっち関数
        if "ソウ" == message.author.name:
            await bot.send_message("ぼっちのソウさん ")
        # おはよう関数
        if mc.startswith("おはよう"):
            m = "Good morning, " + message.author.name
            await bot.send_message(message.channel, m)
        # こんにちは・こんばんは関数
        elif mc.startswith("こんにちは") or mc.startswith("こんばんは"):
            m = "Hi, " + message.author.name  # メッセージを書きます
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await bot.send_message(message.channel, m)
        # 愛してる関数
        elif mc.startswith("好き") or mc.startswith("愛してる"):
            m = "愛してるよ" + message.author.name  # メッセージを書きます
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await bot.send_message(message.channel, m)
        # 友達だよね関数
        elif mc.startswith("マイ！！フレンド！！") or mc.startswith("友達"):
                m = "マイ！！フレンド！！" + message.author.display_name + "！！" 
                await bot.send_message(message.channel, m)
        # kissして関数
        elif mc.startswith("キス") or mc.startswith("ちゅ") or mc.startswith("チュ"):
            m = message.author.name + "(´³`) ㄘゅ:two_hearts:"  # メッセージを書きます
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await bot.send_message(message.channel, m)
        # 神魔登録説明関数
        elif mc.startswith("神魔登録説明"):
            explanation = ("本日の神魔登録を行いたい際には「神魔登録」から始まり「神魔登録1杖剣槍2本槌弓3」のように1,2,3を区切りとして発言してください。"
                        "\nbotから日付と共に「登録完了」と返事が出れば完了です。"
                        "\n「神魔」とだけ言った場合、その日に登録された神魔が通知されます。"
                        "\n「神魔登録説明」でこの説明を繰り返します。")  # 説明
            await bot.send_message(message.channel, explanation)
        # 神魔登録関数
        elif mc.startswith("神魔登録"):  # 「神魔登録」で始まるか調べる
            if mc.count("1")*mc.count("2")*mc.count("3") != 0:
                shinma1 = mc[mc.index("1") + 1: mc.index("2")]  # 第一神魔
                shinma2 = mc[mc.index("2") + 1: mc.index("3")]  # 第二神魔
                date_register = datetime.date.today()  # 神魔登録の日付
                # 登録完了のメッセージ
                await bot.send_message(message.channel, "登録完了 on " + str(date_register))
        # 神魔呼び出し関数
        elif mc.startswith("神魔") and len(mc) == 2:
            if date_today != date_register:  # 直近の神魔登録日が今日ではない場合
                await bot.send_message(message.channel, str(date_today) + "の神魔は登録されていません")
            else:  # 今日神魔が登録されていた場合
                await bot.send_message(message.channel, "第一神魔は{}\n第二神魔は{}".format(shinma1, shinma2))
        await bot.process_commands(message)  # bot.commandも使えるために必要

# 神魔登録をリセットする関数も欲しい？？


@bot.command()
async def roll(dice: str):
    """サイコロを振ることができます。TRPGで使われるNdN記法。2個の6面サイコロの結果がほしい場合は「?roll 2d6」と入力してください。"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say("「NdN」の形じゃないよ！")
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description="For when you wanna settle the score some other way")
async def choose(*choices: str):
    """選択肢からランダムに一つ選びます。「?choose」の後に選択肢をスペースで区切って入力してください。"""
    await bot.say(random.choice(choices))

@bot.command()
async def vc():
    "「コロシアムVC」の参加メンバーの名前一覧を表示します。"
    channel = bot.get_channel("413951021891452932")
    member_list = pprint.pformat(
        [member.name for member in channel.voice_members])
    await bot.say(member_list.replace(",", "\n"))


bot.run('NTA1NDA0OTE4NTI2Mzc4MDA0.DrZwjg.Dpv0JWxtpB8aCcdwW9pymObl914')
