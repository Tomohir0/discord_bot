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

startup_extensions = ["note", "sinoalice", "tool", "system"]  # cogの導入

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


@bot.command(description='sourceは https://github.com/Tomohir0/discord_bot/blob/master/shinma.py を確認してください。')
async def new():
        """最近の更新情報をお知らせします。"""
        m_new = ("Nov,2:cogを導入！開発側としては大分大きいけど、使い手としては関数に分類が付いたくらいかな？callrandをとりあえず追加！メモをランダムに開いちゃおう！王様ゲーム的なのも作れそうかも？"
                 "\nNov,1:長かったからcall_labels=>labelsに変更したよ！役職関連の関数をこれで完備だ！これでお休み一目瞭然！tmp_uoとtmp_dlは内部関数に。"
                 "\nOct,31:ファイルベースをjsonからpickleに！今までのスピードが帰ってきたぜ！！"
                 "\ntmp_upとtmp_dlのときのみS3とやり取りするんだよ！効率的！新しい関数はないけど、毎回出してるとややこしいもんね！"
                 "\nOct,31:役割を忘れすぎているから神魔botに無理やり神魔を思い出させたよ！限定的にpickle復活！"
                 "\nOct,31:s3連携完了だああああ！これでbotを更新してもdataが消えることはなくなったああ！fixし放題だね！"
                 "\nその代わり、ちょっと反応遅くなっちゃったけど許してほしいな……)call_labelsも実装したよ！")
        #m_old = ("\n\nOct,31:ctx実装。役職機能実装。absentを使って役職をAbsentに。role_resetで戻せるから安心して！"
        #     "\nOct,30:pickle実装できたけれど、結局server起動ごとに変数は消えてしまう……。でもserverで共有できるメモ機能のnotesとcallsを実装したよ。")
        #     "\nOct,29:ch_listの一時削除。noteやcallを追加。pickle実験したいなー"
        #     "\nOct,28:ch_listやvc_randを追加。各commandのdescriptionを充実。セリフを感情豊かに"
        m2 = (
            "\n\n過去の更新情報については https://github.com/Tomohir0/discord_bot/blob/master/README ")
        await bot.say(m_new + m2)

@bot.event  # server加入時の処理
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    func_tmp_dl() # まずdl

@bot.event
async def on_message(message):  # 関数名はon_messageのみ
    date_today = datetime.date.today()
    mc = message.content
    id = ["", "", ""]
    stwith_dict = { # 呼応一覧
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
        "お腹すいた":"わかる。めっちゃお腹空いた。"
    }
    if bot.user != message.author:  # botによるbotの反応を避ける
        return 0
    # ぼっち関数など
    if mc.startswith("?"):  # 呼びかけ追加
        if "413309417082322955" == message.author.id:
            await bot.send_message(message.channel, "えっちな{}さん ".format(message.author.name))
    for key in stwith_dict.keys():
       if mc.startswith(key):
           await bot.say(stwith_dict.get(key)) 
    # 神魔関連
    if mc.startswith("神魔"):
        # ぼっち関数
        if "413309417082322955" == message.author.id:
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

@bot.event # error時に定期的にupload
async def on_command_error(exception: Exception, ctx: commands.Context):
    global error_count
    channel = bot.get_channel("505977333182758915")
    error_count += 1
    if error_count%10 == 1 and ctx.message.author.id == "349102495114592258":# 毎回はさすがに多い。他の人のerrorは無視
        func_tmp_up()
        await bot.send_message(channel,"up") # 一人serverに報告

if __name__ == "__main__": # cogへジャンプ
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run('NTA1NDA0OTE4NTI2Mzc4MDA0.DrZwjg.Dpv0JWxtpB8aCcdwW9pymObl914')

