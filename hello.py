import discord

client = discord.Client()

@client.event
async def on_ready():
 print('Logged in as')
 print(client.user.name)
 print(client.user.id)
 print('------')

@client.event
async def on_message(message):
# 「おはよう」で始まるか調べる
 if message.content.startswith("おはよう"):
# 送り主がBotだった場合反応したくないので
  if client.user != message.author:
 # メッセージを書きます
   m = "おはようございます" + message.author.name + "さん！/r/n投票お忘れなく！"
# メッセージが送られてきたチャンネルへメッセージを送ります
   await client.send_message(message.channel, m)

client.run("NTA1MDE0MDQyNzM4Mjk0Nzg1.DrNeBA.dvNe0cvuyZAi9BZPumN8hXCVzzE")
