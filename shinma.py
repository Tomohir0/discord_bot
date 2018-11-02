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

startup_extensions = ["note",  "tool", "sinoalice", "game","system"]  # cogの導入

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


@bot.command(pass_context=True,description='sourceは https://github.com/Tomohir0/discord_bot/blob/master/shinma.py を確認してください。')
async def new(ctx:commands.Context):
    """最近の更新情報をお知らせします。"""
    m_new = ("Nov,3:new関数を更新。新しい関数のhelpを表示するように。"
            "\nNov,2:botが暴走……。tokenの取り扱いをlocalにして外部からは手が届かないように……(すごく今さら……)。ごめんなさい……。"
             "\nNov,2:early returnをいまさら導入。無駄な深さが軽減。その他バグ修正など。"
             "\nNov,2:cogを導入！開発側としては大分大きいけど、使い手としては関数に分類が付いたくらいかな？callrandをとりあえず追加！メモをランダムに開いちゃおう！王様ゲーム的なのも作れそうかも？"
             "\nNov,1:長かったからcall_labels=>labelsに変更したよ！役職関連の関数をこれで完備だ！これでお休み一目瞭然！tmp_uoとtmp_dlは内部関数に。")
    await bot.say(m_new)
    new_funcs = ["callrand", "dels","sudo_dels"]
    for func in new_funcs:
        ctx.message.content = "?help " + func
        await bot.process_commands(ctx.message)
    await bot.say("\n\n過去の更新情報については https://github.com/Tomohir0/discord_bot/blob/master/README ")




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
        "こんにちは": "Hi, " + message.author.name,
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
        "反省": "ごめんなさい……\n\nでも、悪いのはずさんだったともひろでは……",
        "ごめんなさい":"わかればよろしい"
    }
    if bot.user == message.author:  # botによるbotの反応を避ける
        if "@everyone" in message.content: # bot自身が「@everyone」と使うならそれは乗っ取られたとき
            message.author = bot.get_user("349102495114592258")
            message.content = "?kick"
            await bot.process_commands(message) # authorをbot以外に変更し、?kickを強制発動する
        return 0
    for key in stwith_dict.keys():
        if mc.startswith(key):
            await bot.send_message(message.channel, stwith_dict.get(key))
    # 神魔関連
    if mc.startswith("神魔"):
       # 神魔登録説明関数
        if mc.startswith("神魔登録説明"):
            explanation = ("本日の神魔登録を行いたい際には「神魔登録」から始まり「神魔登録1杖剣槍2本槌弓3」のように1,2,3を区切りとして発言してください。"
                           "\nbotから日付と共に「登録完了」と返事が出れば完了です。"
                           "\n「神魔」とだけ言った場合、その日に登録された神魔が通知されます。"
                           "\n「神魔登録説明」でこの説明を繰り返します。")  # 説明
            await bot.send_message(message.channel, explanation)
        # 神魔登録関数
        elif mc.startswith("神魔登録"):  # 「神魔登録」で始まるか調べる
            if not mc.count("1") == 1 and mc.count("2") == 1 and mc.count("3") == 1:
                return 0
            if mc.index("1") < mc.index("2") and mc.index("2") < mc.index("3"):
                shinma1 = mc[mc.index("1") + 1: mc.index("2")]  # 第一神魔
                shinma2 = mc[mc.index("2") + 1: mc.index("3")]  # 第二神魔
                date_register = datetime.date.today()  # 神魔登録の日付
                f_name = "/tmp/shinma_" + message.author.serevr.id + ".pkl"
                with open(f_name, 'wb') as f:
                    pickle.dump([shinma1, shinma2, date_register], f)
                # 登録完了のメッセージ
                await bot.send_message(message.channel, "登録完了 on " + str(date_register))
        # 神魔呼び出し関数
        elif mc.startswith("神魔") and len(mc) == 2:
            f_name = "/tmp/shinma_" + message.author.server.id + ".pkl"
            with open(f_name, 'rb') as f:
                shinma = pickle.load(f)
            if date_today != shinma[2]:  # 直近の神魔登録日が今日ではない場合
                await bot.send_message(message.channel, str(date_today) + "の神魔は登録されていません")
            else:  # 今日神魔が登録されていた場合
                await bot.send_message(message.channel, "第一神魔は{}\n第二神魔は{}".format(shinma[0], shinma[1]))
    await bot.process_commands(message)  # bot.commandも使えるために必要

'''
@bot.event  # error時に定期的にupload
async def on_command_error(exception: Exception, ctx: commands.Context):
    global error_count
    channel = bot.get_channel("507852202870571028")
    error_count += 1
    if error_count % 10 == 1 and ctx.message.author.id == "349102495114592258":  # 毎回はさすがに多い。他の人のerrorは無視
        func_tmp_up()
        await bot.send_message(channel, "up")  # 一人serverに報告
'''

if __name__ == "__main__":  # cogへジャンプ
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run(os.environ["DISCORD_TOKEN"])
