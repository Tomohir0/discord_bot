import discord
import datetime

client = discord.Client()
date_today = datetime.date.today()
date_register = "2000-01-01"
shinma1 = ""
shinma2 = ""
# async外で保存するためにGlobal変数を用いる


@client.event  # server加入時
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):  # 関数名はon_messageのみ
    global date_register, shinma1, shinma2  # Global宣言
    # おはよう関数
    if message.content.startswith("おはよう"):
        if client.user != message.author:
            m = "Good morning, " + message.author.name  # メッセージを書きます
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)
    # こんにちは・こんばんは関数
    elif message.content.startswith("こんにちは") or message.content.startswith("こんばんは"):
        if client.user != message.author:
            m = "Hi, " + message.author.name  # メッセージを書きます
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)
    # 愛してる関数
    elif message.content.startswith("好き") or message.content.startswith("愛してる"):
        if client.user != message.author:
            m = "愛してるよ" + message.author.name  # メッセージを書きます
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)
    # 友達だよね関数
    elif message.content.startswith("マイ！！フレンド！！"):
        if client.user != message.author:
            m = "マイ！！フレンド！！" + message.author.name + "！！"  # メッセージを書きます
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)
    elif message.content.startswith("キスして") or message.content.startswith("ちゅーして"):
        if client.user != message.author:
            m = message.author.name + "(´³`) ㄘゅ:two_hearts:"  # メッセージを書きます
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)
    # 神魔登録説明関数
    elif message.content.startswith("神魔登録説明"):
        if client.user != message.author:
            explanation = ("本日の神魔登録を行いたい際には「神魔登録」から始まり「神魔登録1杖剣槍2本槌弓3」のように1,2,3を区切りとして発言してください。"
                           "\nbotから日付と共に「登録完了」と返事が出れば完了です。"
                           "\n「神魔」とだけ言った場合、その日に登録された神魔が通知されます。"
                           "\n「神魔登録説明」")  # 説明
            await client.send_message(message.channel, explanation)
    # 神魔登録関数
    elif message.content.startswith("神魔登録"):  # 「神魔登録」で始まるか調べる
        if client.user != message.author:  # 送り主がBotだった場合反応したくないので
            m = message.content
            if m.count("1")*m.count("2")*m.count("3") != 0:
                shinma1 = m[m.index("1") + 1: m.index("2")]  # 第一神魔
                shinma2 = m[m.index("2") + 1: m.index("3")]  # 第二神魔
                date_register = datetime.date.today()  # 神魔登録の日付
                # 登録完了のメッセージ
                await client.send_message(message.channel, "登録完了 on " + str(date_register))
    # 神魔呼び出し関数
    elif message.content.startswith("神魔") and len(message.content) == 2:
        if client.user != message.author:  # botかどうか
            if date_today != date_register:  # 直近の神魔登録日が今日ではない場合
                await client.send_message(message.channel, str(date_today) + "の神魔は登録されていません")
            else:  # 今日神魔が登録されていた場合
                await client.send_message(message.channel, "第一神魔は{}\n第二神魔は{}".format(shinma1, shinma2))

client.run("NTA1NDA0OTE4NTI2Mzc4MDA0.DrTU3A.vEAG95sW7-oWEPpGNwpr-9wBvtQ")

# 神魔登録をリセットする関数も欲しい？？
