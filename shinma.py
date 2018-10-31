import discord
import datetime
import pprint
import random

import os
import pickle

from discord.ext import commands

import json
import boto3
bucket_name = "tomo-discord"
s3 = boto3.resource('s3')
# s3連携

description = ('''神魔管理のために作られたbotです。挨拶をしたり愛をささやいたりもします。
\n「神魔登録説明」で神魔登録などについての説明を表示します。\nその他のcommandについては「?help」を確認してください。「?」を文頭に置いて適宜使用できます。''')
bot = commands.Bot(command_prefix='?', description=description)

id = ["0", "0", "0"]  # server,channel,author
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
    global id  # Global宣言
    mc = message.content
    if bot.user != message.author:  # botによるbotの反応を避ける
        id[0] = message.server.id
        id[1] = message.channel.id
        id[2] = message.author.id  # commandのためにid用意。天才
        # ぼっち関数など
        if mc.startswith("?"):  # 呼びかけ追加
            if "413309417082322955" == id[2]:
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
        elif mc.startswith("おなかすいた") or mc.startswith("お腹空いた") or mc.startswith("お腹すいた"):
            m = "わかる。めっちゃお腹空いた。"
            await bot.send_message(message.channel, m)
        # 神魔関連
        if mc.startswith("神魔"):
            # ぼっち関数
            if "413309417082322955" == id[2]:
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
                if mc.count("1") == 1 and mc.count("2") == 1 and mc.count("3") == 1:
                    if mc.index("1") < mc.index("2") and mc.index("2") < mc.index("3"):
                        shinma1 = mc[mc.index("1") + 1: mc.index("2")]  # 第一神魔
                        shinma2 = mc[mc.index("2") + 1: mc.index("3")]  # 第二神魔
                        date_register = datetime.date.today()  # 神魔登録の日付
                        f_name = "/tmp/shinma_" + id[0] + ".pkl"
                        with open(f_name, 'wb') as f:
                            pickle.dump([shinma1, shinma2, date_register], f)
                        # 登録完了のメッセージ
                        await bot.send_message(message.channel, "登録完了 on " + str(date_register))
            # 神魔呼び出し関数
            elif mc.startswith("神魔") and len(mc) == 2:
                f_name = "/tmp/shinma_" + id[0] + ".pkl"
                with open(f_name, 'rb') as f:
                    shinma = pickle.load(f)
                if date_today != shinma[2]:  # 直近の神魔登録日が今日ではない場合
                    await bot.send_message(message.channel, str(date_today) + "の神魔は登録されていません")
                else:  # 今日神魔が登録されていた場合
                    await bot.send_message(message.channel, "第一神魔は{}\n第二神魔は{}".format(shinma[0], shinma[1]))
        await bot.process_commands(message)  # bot.commandも使えるために必要

# 神魔登録をリセットする関数も欲しい？？


@bot.command(description='sourceは https://github.com/Tomohir0/discord_bot/blob/master/shinma.py を確認してください。')
async def new():
    """最近の更新情報をお知らせします。"""
    m_new = ("Oct,31:s3連携完了だああああ！これでbotを更新してもdataが消えることはなくなったああ！fixし放題だね！")
    m_old = ("\nOct,31:ctx実装。役職機能実装。absentを使って役職をAbsentに。role_reset_allで戻せるから安心して！"
         "\nOct,30:pickle実装できたけれど、結局server起動ごとに変数は消えてしまう……。でもserverで共有できるメモ機能のnotesとcallsを実装したよ。"
         "\nOct,29:ch_listの一時削除。noteやcallを追加。pickle実験したいなー"
         "\nOct,28:ch_listやvc_randを追加。各commandのdescriptionを充実。セリフを感情豊かに")
    m2 = ("\n\n過去の更新情報については https://github.com/Tomohir0/discord_bot/blob/master/README ")
    await bot.say(m_new + m_old + m2)


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
    if random.randint(1, 2) == 1:
        await bot.say(random.choice(choices) + "にするしかないじゃない！")
    else:
        await bot.say("ﾀﾞﾗﾗﾗﾗﾗﾗﾗﾗﾗ～\nダン！！\n見事選ばれたのは" + random.choice(choices) + "でした！！")


@bot.command(description='「?vc」で「コロシアムVC」の参加メンバーの(ニックネームではない)名前一覧が得られます。')
async def vc():
    "「コロシアムVC」の参加メンバーの名前一覧を表示します。"
    channel = bot.get_channel("413951021891452932")
    if len([member.name for member in channel.voice_members]) == 0:
        await bot.say("今、" + channel.name + "には一人もいない……一人も……")
    else:
        member_list = pprint.pformat(
            [member.name for member in channel.voice_members])
        # replaceで改行して見やすく
        await bot.say(channel.name + "にいるのは\n" + member_list.replace(",", "\n") + "\nだよ！")


@bot.command(description='serverのみんなでmemoを共有できます。', pass_context=True)
async def notes(ctx: commands.Context, label: str, *, memo: str):
    "「?notes secret ギルマスは実は高校生」とすれば、secretラベルで「ギルマスは実は高校生」を記録できます。スペースが区切りとみなされます"
    json_key = "memo_" + ctx.message.author.server.id + ".json" # 読み出し
    obj = s3.Object(bucket_name, json_key)
    memos = json.loads(obj.get()['Body'].read())  # s3からjson => dict
    memos[label] = memo # 追加
    obj.put(Body=json.dumps(memos))
    await bot.say("覚えました！！")



@bot.command(description='「?notes」で保存されたmemoを読み出すことができます。', pass_context=True)
async def calls(ctx: commands.Context, label: str):
    "「?calls secret」でsecretとして保存されたメモを読み出します。"
    json_key = "memo_" + ctx.message.author.server.id + ".json"
    obj = s3.Object(bucket_name, json_key)
    memos = json.loads(obj.get()['Body'].read())  # s3からjson => dict
    await bot.say(memos[label])



@bot.ccomand(description=' ', pass_context=True)
async def call_labels(ctx: commands.Context):
    "「?notes」のlabelの一覧を表示します。"
    json_key = "memo_" + ctx.message.author.server.id + ".json"
    obj = s3.Object(bucket_name, json_key)
    memos = json.loads(obj.get()['Body'].read())  # s3からjson => dict
    await bot.say(pprint.pformat(memos.keys()).replace(",","\n"))


@bot.command(description='「?vc_rand 2」で「コロシアムVC」の参加メンバーから二人を選びます。')
async def vc_rand(num: int):
    "「コロシアムVC」の参加メンバーの中からランダムに指定された人数を選びます。"
    channel = bot.get_channel("413951021891452932")
    member_list = [member.display_name for member in channel.voice_members]
    if len(member_list) < num or num < 1:
        await bot.say("変だよ！\n今のVCには{}人しかいないのに、人数指定が{}人は変だよ！".format(len(member_list), num))
    else:
        await bot.say(random.sample(member_list, num) + "！\n君に決めた！")



@bot.command(description=' ', pass_context=True)
async def absent(ctx: commands.Context):
    "役職をAbsentに変更して遅刻しそうないし欠席の可能性があることを明確にできます。「?role_reset」で全員のAbsentをもとに戻せます。"
    user = ctx.message.author
    role = discord.utils.get(user.server.roles, name="Absent")
    await bot.add_roles(user, role)


@bot.command(description=' ', pass_context=True)
async def role_reset_single(ctx: commands.Context):
    "あなた一人の役職を@everyoneに戻せます。"
    user = ctx.message.author
    role = discord.utils.get(user.server.roles, name="@everyone")
    await bot.add_roles(user, role)


@bot.command(description=' ', pass_context=True)
async def role_reset_all(ctx: commands.Context):
    "Absentの人の役職をすべて@everyoneに戻せます。"
    user = ctx.message.author
    role = discord.utils.get(user.server.roles, name="@everyone")
    for member in user.server.members:
        if member.role.name == "Absent":
            await bot.add_roles(member, role)

bot.run('NTA1NDA0OTE4NTI2Mzc4MDA0.DrZwjg.Dpv0JWxtpB8aCcdwW9pymObl914')

