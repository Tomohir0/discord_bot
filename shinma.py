import discord
import datetime
import pprint
import random

import pickle

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
        if mc.startswith("?"):  # 呼びかけ追加
            if "413309417082322955" == message.author.id:
                await bot.send_message(message.channel, "ぼっちの{}さん ".format(message.author.name))
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
        elif mc.startswith("キス") or mc.startswith("ちゅ") or mc.startswith("チュ") or mc.startswith("kiss"):
            m = message.author.name + "(´³`) ㄘゅ:two_hearts:"  # メッセージを書きます
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await bot.send_message(message.channel, m)
        # 神魔関連
        if mc.startswith("神魔"):
            # ぼっち関数
            if "413309417082322955" == message.author.id:
                await bot.send_message(message.channel, "ぼっちの{}さん ".format(message.author.name))
            # 神魔登録説明関数
            if mc.startswith("神魔登録説明"):
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


@bot.command(description='過去の更新情報はhttps://github.com/Tomohir0/discord_botのshinma.pyのHistoryやREADMEを確認してください。')
async def new():
    """最近の更新情報をお知らせします。"""
    m = ("Oct,29:ch_listの一時削除。noteやcallを追加。pickle実験したいなー"
    "\nOct,28:ch_listやvc_randを追加。各commandのdescriptionを充実。セリフを感情豊かに")
    await bot.say(m)


@bot.command(description='「?roll 2d6」で「3, 5」などが得られます。')
async def roll(dice: str):
    """サイコロを振ることができます。TRPGで使われるNdN記法。2個の6面サイコロの結果がほしい場合は「?roll 2d6」と入力してください。"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say("「NdN」の形じゃないよ！")
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say("ダイスロール！\n" + result)


@bot.command(description='「?choice A B C」などのように入力してください。')
async def choose(*choices: str):
    """選択肢からランダムに一つ選びます。「?choose」の後に選択肢をスペースで区切って入力してください。"""
    await bot.say(random.choice(choices) + "にするしかないじゃない！")


@bot.command(description='「?vc」で「コロシアムVC」の参加メンバーの(ニックネームではない)名前一覧が得られます。')
async def vc():
    "「コロシアムVC」の参加メンバーの名前一覧を表示します。"
    channel = bot.get_channel("413951021891452932")
    if len([member.name for member in channel.voice_members]) == 0:
        await bot.say("今、" + channel.name + "には一人もいない……一人も……")
    else:
        member_list = pprint.pformat(
            [member.name for member in channel.voice_members])
        await bot.say(channel.name + "にいるのは\n" + member_list.replace(",", "\n") + "\nだよ！")


'''
@bot.command(description='チャンネルidは別commandで使用することができるかもしれません。')
async def ch_list():
    "各チャンネルの名前とidの組を表示します。"
    channel_id = [channel.id for channel in bot.get_all_channels()]
    channel_name = [channel.name for channel in bot.get_all_channels()]
    await bot.say("チャンネル一覧を表示するよ！メモの用意はできたかな？")
    for (name, id) in zip(channel_name, channel_id):
        await bot.say(name+", " + id)
'''

@bot.command(description='「?vc_rand 2」で「コロシアムVC」の参加メンバーから二人を選びます。')
async def vc_rand(num: int):
    "「コロシアムVC」の参加メンバーの中からランダムに指定された人数を選びます。"
    channel = bot.get_channel("413951021891452932")
    member_list = [member.display_name for member in channel.voice_members]
    if len(member_list) < num or num < 1:
        await bot.say("変だよ！\n今のVCには{}人しかいないのに、人数指定が{}人は変だよ！".format(len(member_list), num))
    else:
        await bot.say(random.sample(member_list, num) + "！\n君に決めた！")


@bot.command()
async def write(memo: str):
    "メモを記録します。「?call」で呼び出します。"
    global note
    note = memo
    await bot.say("覚えました！！")

@bot.command()
async def call():
    "「?write」で記録したメモを呼び出します。"
    global note
    await bot.say(note)


@bot.command()
async def writep(memo: str):
    "メモを記録します。「?call」で呼び出します。"
    f = open('/tmp/memo.pkl', 'wb')
    pickle.dump(memo,f)
    await bot.say("覚えました！！")
    memo2 = pickle.load(f)
    await bot.say(memo2)


@bot.command()
async def callp():
    "「?write」で記録したメモを呼び出します。"
    f = open('/tmp/memo.pkl', 'rb')
    memo = pickle.load(f)
    await bot.say(memo)

bot.run('NTA1NDA0OTE4NTI2Mzc4MDA0.DrZwjg.Dpv0JWxtpB8aCcdwW9pymObl914')
