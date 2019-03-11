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

startup_extensions = ["note",  "tool",
                      "sinoalice", "game", "system", "exp"]  # cogの導入

description = ("ともひろのdiscordのbotです。いろいろあって2代目です"
               "\ncommandについては「?help」を確認してください。"
               "「?」を文頭に置いて適宜使用できます。"
               "\nscriptは https://github.com/Tomohir0/discord_bot/blob/master/shinma.py")
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
        "おはよ": "Good morning, " + message.author.name,
        "こんにち": "Hi, " + message.author.name,
        "こんばんは": "Hi, " + message.author.name,
        "好き": "愛してるよ" + message.author.name,
        "愛してる": "愛してるよ" + message.author.name,
        "おなかすいた": "わかる。めっちゃお腹空いた。",
        "お腹空いた": "わかる。めっちゃお腹空いた。",
        "お腹すいた": "わかる。めっちゃお腹空いた。",
        "ごめんなさい": "わかればよろしい",
        "おかえり": "ただいま！",
        "おやす": "いい夢を……"+message.author.name + "ちゃん",
    }
    if bot.user == message.author:  # botによるbotの反応を避ける
        # bot自身が「@everyone」と2回も使うならそれは乗っ取られたとき
        if message.content.count("@everyone") > 1:
            message.author = bot.get_user("349102495114592258")
            message.content = "?bot_kick"
            # authorをbot以外に変更し、?kickを強制発動する
            await bot.process_commands(message)
        return 0

    forbidden_channels = []
    if message.channel.id in forbidden_channels:  # 指定されたchannelではbotはお静かに
        return 0

    for key in stwith_dict.keys():
        if mc.startswith(key):
            await bot.send_message(message.channel, stwith_dict.get(key))
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
