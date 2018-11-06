import discord
import time

now_time = time.time()
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # 「こん」で始まるか調べる
    if message.content.startswith("こん"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージを書きます
            #   m = "Hello, ほも" + message.author.name + ""
            m = "Hi, " + message.author.name + "投票し忘れてるでゲソ"
# メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)
    elif message.content.startswith("おはよう"):
        if client.user != message.author:
            # メッセージを書きます
            m = "Good morning, " + message.author.name + "投票し忘れてるでゲソ"
# メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)

client.run("")
