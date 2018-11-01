import discord
from discord.ext import commands
import datetime
import pprint
import random

import os
import pickle
import glob

import boto3
bucket_name = "tomo-discord"
s3 = boto3.resource('s3')
# s3連携

extension_list = ["note", "sinoalice", "tool", "system"]
startup_extensions = extension_list # cogの導入

description = ("神魔管理のために作られたbotです。挨拶をしたり愛をささやいたりもします。"
                "\n「神魔登録説明」で神魔登録などについての説明を表示します。\nその他のcommandについては「?help」を確認してください。"
                "「?」を文頭に置いて適宜使用できます。"
                "\nCategoryとしては"+ pprint.pformat(extension_list) + "があります。"
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
        #await bot.say(file_name)
        # "/tmp/"のままではs3においては""(空欄)ディレクトリ内のtmpディレクトリにアクセスしてしまう
        s3.Object(bucket_name, file_name[1:]).upload_file(file_name)
    #await bot.say("Upload's Finished")

def func_tmp_dl():
    "s3からtmpフォルダにfileを復帰させます。(download)"
    client = boto3.client('s3')
    # "/tmp/"のままではs3においては""(空欄)ディレクトリ内のtmpディレクトリにアクセスしてしまう
    response = client.list_objects(Bucket=bucket_name, Prefix="tmp/")
    file_list = [content['Key'] for content in response['Contents']]
    for file_name in file_list:
        #await bot.say(file_name)
        s3.Object(bucket_name, file_name).download_file("/"+file_name)
    #await bot.say("Download's Finished")


@bot.event  # server加入時の処理
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    func_tmp_dl()

@bot.event
async def on_message(message):  # 関数名はon_messageのみ
    date_today = datetime.date.today()
    mc = message.content
    id = ["", "", ""]
    if bot.user != message.author:  # botによるbotの反応を避ける
        id[0] = message.server.id
        id[1] = message.channel.id
        id[2] = message.author.id  # commandのためにid用意。天才
        # ぼっち関数など
        if mc.startswith("?"):  # 呼びかけ追加
            if "413309417082322955" == id[2]:
                await bot.send_message(message.channel, "えっちな{}さん ".format(message.author.name))

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
                await bot.send_message(message.channel, "えっちな{}さん ".format(message.author.name))
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

@bot.event # error時に定期的にupload
async def on_command_error(exception: Exception, ctx: commands.Context):
    global error_count
    channel = bot.get_channel("505977333182758915")
    error_count += 1
    if error_count%10 == 1 and ctx.message.author.id == "349102495114592258":
        func_tmp_up()
        await bot.send_message(channel,"up")

if __name__ == "__main__": # cogへジャンプ
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run('NTA1NDA0OTE4NTI2Mzc4MDA0.DrZwjg.Dpv0JWxtpB8aCcdwW9pymObl914')

