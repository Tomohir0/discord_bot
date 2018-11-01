import discord
import datetime
import pprint
import random
from discord.ext import commands
import pickle
import os

import json
import boto3
bucket_name = "tomo-discord"
s3 = boto3.resource('s3')
#s3連携

startup_extensions = ["note","sinoalice","tool","system"]

description = ('''Test用\nその他のcommandについては「?help」を確認してください。「?」を文頭に置いて適宜使用できます。''')
bot = commands.Bot(command_prefix='?', description=description)
date_today = datetime.date.today()
date_register = "2000-01-01"
# async外で保存するためにGlobal変数を用いる


@bot.event  # server加入時の処理
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):  # 関数名はon_messageのみ
    id=["", "", ""]
    date_today = datetime.date.today()
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

@bot.command()
async def roll(dice: str):
    """サイコロの結果を得ることができます。TRPGで使われるNdN記法を採用しています。2個の6面サイコロの結果がほしい場合は「?roll 2d6」と入力してください。"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('「NdN」の形じゃないよ！')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command(description='「?vc」で「コロシアムVC」の参加メンバーの(ニックネームではない)名前一覧が得られます。',pass_context=True)
async def vvc(ctx: commands.Context):
    "「コロシアムVC」の参加メンバーの名前一覧を表示します。"
    channel = bot.get_channel("385094571383848965")
    if len([member.name for member in channel.voice_members]) == 0:
        await bot.say("今、" + channel.name + "には一人もいない……一人も……")
    else:
        member_list = pprint.pformat(
            [member.name for member in channel.voice_members])
        # replaceで改行して見やすく
        await bot.say(channel.name + "にいるのは\n" + member_list.replace(",", "\n") + "\nだよ！")

'''
@bot.command(description='「?choice A B C」などのように入力してください')
async def choose(*choices: str):
    """ランダムに一つ選びます。「?choose」の後に選択肢をスペースで区切って入力してください。"""
    await bot.say(random.choice(choices))


@bot.command(description='「?vc_rand 2」で「コロシアムVC」の参加メンバーから二人を選びます。')
async def vc_rand(num: int):
    "「コロシアムVC」の参加メンバーのからランダムに指定された人数を選びます。"
    channel = bot.get_channel("385094571824119818")
    member_list = [member.display_name for member in channel.voice_members]
    if len(member_list) < num or num < 1:
        await bot.say("変だよ！\n今のVCには{}人しかいないのに、人数指定が{}人は変だよ！".format(len(member_list), num))
    else:
        await bot.say(random.sample(member_list, num))


@bot.command()
async def add(num1: int, num2: int):
    await bot.say(str(num1 + num2))


@bot.group(pass_context = True)
async def absent(ctx: commands.Context):
    "あなたがその日に欠席する場合は「?absent」の後に「me」と入力してください。他の人の場合は一覧から対応する数字を入力してください。"
#    global id
#    name_list = [member.name for member in bot.get_all_members()]
#    id_list = [member.id for member in bot.get_all_members()]
#    name = name_list[id_list.index(id[2])]
    if ctx.invoked_subcommand is None:
        await bot.say("以下のリストから名前を探して、その横にある数字をこたえてね。その人の欠席を登録するよ！あなた自身の場合は「me」でOK!")
#        for name_tmp in name_list:
#            m += str(name_list.index(name_tmp) + 1) + ", " + name_tmp + "\n"
        await bot.say("さあ、数字または「me」を入力してね！")

@absent.command(me_or_number="me", pass_context=True)
async def absent_me(ctx: commands.Context):
#    user = ctx.message.author
#    absent_list[id_list.index(user.id)] = "absent"
    await bot.say("はお休み！")

@absent.command(me_or_number="1", pass_context=True)
async def absent_other(ctx: commands.Context):
    await bot.say("OK")

'''
# bot.group dont go well...

@bot.command()
async def show_role():
    roles = pprint.pformat(discord.Role)
    await bot.say(roles.replace(",","\n"))


@bot.command(pass_context=True)
async def get_roles(ctx):
    user = ctx.message.author
    await bot.say(user.name)
    if user.role.name != "Absent":
        role = discord.utils.get(user.server.roles, name="Absent")
        await bot.say(role.name)
        await bot.add_roles(user, role)
        await bot.say(user.name)


@bot.command(description=' ', pass_context=True)
async def presents(ctx: commands.Context):
    "あなた一人の役職をAbsentから戻します。"
    user = ctx.message.author
    role = discord.utils.get(user.server.roles, name="Absent")
    await bot.remove_roles(user, role)


@bot.command()
async def note(memo: str):
    "メモを記録します。「?call」で呼び出します。"
    json_key = "memo.json"
    obj = s3.Object(bucket_name, json_key)
    obj.put(Body=json.dumps({"1":memo}))
    await bot.say("覚えました！！")


@bot.command()
async def call():
    "「?note」で記録したメモを呼び出します。"
    json_key = "memo.json"
    obj = s3.Object(bucket_name, json_key)
    memos = json.loads( obj.get()['Body'].read())
    await bot.say(memos["1"])

'''
@bot.command(description='serverのみんなでmemoを共有できます。', pass_context=True)
async def notess(ctx: commands.Context, label: str, *, memo: str):
    "「?notes secret ギルマスは実は高校生」とすれば、secretラベルで「ギルマスは実は高校生」を記録できます。ラベル名は英数字のみ。スペースが区切りとみなされます"
    f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
    if not os.path.isfile(f_name):  # 存在しないときの処理
        memos = {}
    else:
        with open(f_name, 'rb') as f:
            memos = pickle.load(f)
    memos[label] = memo
    with open(f_name, 'wb') as f:
        pickle.dump(memos, f)  # 古いリストに付け足す形で
    await bot.say("覚えました！！")
    

@bot.command(description='「?notes」で保存されたmemoを読み出すことができます。', pass_context=True)
async def callss(ctx: commands.Context, label: str):
    "「?calls secret」でsecretとして保存されたメモを読み出します。"
    f_name = "/tmp/memos_" + ctx.message.author.server.id + ".pkl"
    if not os.path.isfile(f_name):  # 存在しないときの処理
        await bot.say("まだこのserverにはメモがないよ……。?notesを使ってほしいな……")
    else:
        with open(f_name, 'rb') as f:
            memos = pickle.load(f)
            await bot.say(memos.get(label, label + "なんてlabelのメモないよ！"))
    
'''

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run('NTA1NjYxMTE3NjIwNTUxNjgx.DrW1Uw.KC36a1LyMlHdYoHtnSS-X2802EM')
