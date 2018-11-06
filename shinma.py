import discord
from discord.ext import commands
import datetime
import pprint
#import random
#import asyncio

import numpy
import os
import pickle
import glob
import numpy as np

import boto3
bucket_name = "tomo-discord"
s3 = boto3.resource('s3')
# s3連携

startup_extensions = ["note",  "tool", "sinoalice", "game","system","exp"]  # cogの導入

description = ("神魔管理のために作られたbotです。挨拶をしたり愛をささやいたりもします。"
               "\n「神魔登録説明」で神魔登録などについての説明を表示します。\nその他のcommandについては「?help」を確認してください。"
               "「?」を文頭に置いて適宜使用できます。"
               "\nsourceは https://github.com/Tomohir0/discord_bot/blob/master/shinma.py")
bot = commands.Bot(command_prefix='?', description=description)

error_count = 0
# async外で保存するためにGlobal変数を用いる

'''
s3 function
'''


def func_tmp_up():
    "tmpフォルダ内のfileをs3に避難させます(upload)。"
    for file_name in glob.glob("/tmp/*.*"):
        # await bot.say(file_name)
        # "/tmp/"のままではs3においては""(空欄)ディレクトリ内のtmpディレクトリにアクセスしてしまう
        s3.Object(bucket_name, file_name[1:]).upload_file(file_name)
    # await bot.say("Upload's Finished")

def func_tmp_dl():
    "s3からtmpフォルダにfileを復帰させます。(download)"
    client = boto3.client('s3')
    # "/tmp/"のままではs3においては""(空欄)ディレクトリ内のtmpディレクトリにアクセスしてしまう
    response = client.list_objects(Bucket=bucket_name, Prefix="tmp/")
    file_list = [content['Key'] for content in response['Contents']]
    for file_name in file_list:
        # await bot.say(file_name)
        s3.Object(bucket_name, file_name).download_file("/"+file_name)
    # await bot.say("Download's Finished")

@bot.event  # server加入時の処理
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    func_tmp_dl()  # まずdl

@bot.event
async def on_message(message):  # 関数名はon_messageのみ
    date_today = datetime.date.today()
    mc = message.content
    stwith_dict = {  # 呼応一覧
        "おはよ": "Good morning" + message.author.name,
        "こんにち": "Hi, " + message.author.name,
        "こんばんは": "Hi, " + message.author.name,
        "好き": "愛してるよ" + message.author.name,
        "愛してる": "愛してるよ" + message.author.name,
        "マイ！！フレンド！！": "マイ！！フレンド！！" + message.author.display_name,
        "友達": "マイ！！フレンド！！" + message.author.display_name,
        "キス": "(´³`) ㄘゅ:two_hearts:" + message.author.name,
        "kiss": "(´³`) ㄘゅ:two_hearts:" + message.author.name,
        "ちゅ": "(´³`) ㄘゅ:two_hearts:" + message.author.name,
        "チュ": "(´³`) ㄘゅ:two_hearts:" + message.author.name,
        "おなかすいた": "わかる。めっちゃお腹空いた。",
        "お腹空いた": "わかる。めっちゃお腹空いた。",
        "お腹すいた": "わかる。めっちゃお腹空いた。",
        "ごめんなさい": "わかればよろしい",
        "おかえり": "ただいま！",
        "おやす":"いい夢を……"+message.author.name + "ちゃん"
    }
    if bot.user == message.author:  # botによるbotの反応を避ける
        if message.content.count("@everyone") > 1: # bot自身が「@everyone」と2回も使うならそれは乗っ取られたとき
            message.author = bot.get_user("349102495114592258")
            message.content = "?bot_kick"
            await bot.process_commands(message) # authorをbot以外に変更し、?kickを強制発動する
        return 0

    forbidden_channels = ["507850575921020928",
                          "507850635262033925", "443230542167670790", "507850713175556107"]  
    if message.channel.id in forbidden_channels:  # 指定されたchannelではbotはお静かに
        return 0

    for key in stwith_dict.keys():
        if mc.startswith(key):
            await bot.send_message(message.channel, stwith_dict.get(key))
    
    '''if mc.startswith("おかえりなさい、しんまくん") and message.author.id == "349102495114592258":
        m = ("みなさん、先日はお騒がせしました。あの件を受けともひろもようやくずさんだった管理体制を整え、もしものための自害プログラムも実装しました。"
            "\nまた、実はみなさんから姿を隠している間も数々のcommandが実装されており、今では?helpがログ流しに役立ってしまうほどです。追々説明していければと思います。ともひろにそれ用のcommand作らせます。"
            "\nそれではみなさん、また改めてよろしくお願いします！")
        await bot.send_message(message.channel,m)'''


    # 神魔関連
    if mc.startswith("神魔"):
       # 神魔登録説明関数
        if mc.startswith("神魔登録説明"):
            explanation = ("本日の神魔登録を行いたい際にはまずは「神魔登録」と入力してください。"
                           "\nbotから日付と共に「登録完了」と返事が出れば完了です。"
                           "\n「?reg 第1神魔 第2神魔」でも神魔登録できます。"
                           "\n「神魔」とだけ言った場合、その日に登録された神魔が通知されます。"
                           "\n「神魔登録説明」でこの説明を繰り返します。")  # 説明
            await bot.send_message(message.channel, explanation)
        # 神魔登録関数
        elif mc.startswith("神魔登録"):  # 「神魔登録」で始まるか調べる
            def check(msg):
                return msg.author == message.author
            await bot.send_message(message.channel, "神魔登録を始めよう！\nまずは第1神魔を入力してね！")
            shinma1 = await bot.wait_for_message(check=check) # 神魔入力
            await bot.send_message(message.channel, "次は第2神魔！")
            shinma2 = await bot.wait_for_message(check=check)
            message.content="?reg "+shinma1.content +" "+shinma2.content
            await bot.process_commands(message) # reg起動
        # 神魔呼び出し関数
        elif mc.startswith("神魔") and len(mc) == 2:
            f_name = "/tmp/memos_" + message.author.server.id + ".pkl"
            if not os.path.isfile(f_name):  # 存在しないときの処理
                await bot.send_message(message.channel, str(date_today) + "の神魔は登録されてないよ……登録してほしいな……")
                return 0
            with open(f_name, 'rb') as f:
                memos = pickle.load(f)
            # 直近の神魔登録日が今日ではない場合
            content = memos.get("shinma") # shinma labelがない場合も日付エラーに含む
            if content[:len("YYYY-MM-DD")] != str(date_today):
                await bot.send_message(message.channel, str(date_today) + "の神魔は登録されてないよ……登録してほしいな……")
            else:  # 今日神魔が登録されていた場合
                await bot.send_message(message.channel, content)
    await bot.process_commands(message)  # bot.commandも使えるために必要


@bot.event  # error時に定期的にupload
async def on_command_error(exception: Exception, ctx: commands.Context):
    global error_count
    channel = bot.get_channel("507852202870571028")
    error_count += 1
    if error_count % 10 == 1 and ctx.message.author.id == "349102495114592258":  # 毎回はさすがに多い。他の人のerrorは無視
        func_tmp_up()
        await bot.send_message(channel, "up")  # 一人serverに報告


if __name__ == "__main__":  # cogへジャンプ
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run(os.environ["DISCORD_TOKEN"])
