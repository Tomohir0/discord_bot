import discord
from discord.ext import commands
import pprint
import os
#import pickle

import glob
import boto3
bucket_name = "tomo-discord"
s3 = boto3.resource('s3')
# s3連携


class System():
    "system上存在する関数だよ！みんなの前ではあまり使われないかも！"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='bot再起動する前に使用して、tmpフォルダ内のファイルが失われるのを防ぎましょう。', pass_context=True)
    async def tmp_up(self,ctx: commands.Context):
        "tmpフォルダ内のfileをs3に避難させます(upload)。"
        for file_name in glob.glob("/tmp/*.*"):
            await self.bot.say(file_name)
            # "/tmp/"のままではs3においては""(空欄)ディレクトリ内のtmpディレクトリにアクセスしてしまう
            s3.Object(bucket_name, file_name[1:]).upload_file(file_name)
        await self.bot.say("Finished")

    @commands.command(description='bot再起動後に使用して、tmpフォルダ内にあるべきファイルを復活させましょう。', pass_context=True)
    async def tmp_dl(self, ctx: commands.Context):
        "s3からtmpフォルダにfileを復帰させます。(download)"
        client = boto3.client('s3')
        # "/tmp/"のままではs3においては""(空欄)ディレクトリ内のtmpディレクトリにアクセスしてしまう
        response = client.list_objects(Bucket=bucket_name, Prefix="tmp/")
        file_list = [content['Key'] for content in response['Contents']]
        for file_name in file_list:
            await self.bot.say(file_name)
            s3.Object(bucket_name, file_name).download_file("/"+file_name)
        await self.bot.say("Finished")

    @commands.group(description='', pass_context=True)
    async def storage(self, ctx: commands.Context):
        "herokuおよびs3のtmp内を確認できます。"
        await self.bot.say("storageを確認したいなら「heroku」または「s3」")
        storage = await self.bot.wait_for_message()
        if storage == "s3": 
            "s3のtmpフォルダの中を確認します"
            client = boto3.client('s3')
            response = client.list_objects(Bucket=bucket_name, Prefix="tmp/")
            file_list = [content['Key'] for content in response['Contents']]
            for file_name in file_list:
                await self.bot.say(file_name)
            await self.bot.say("Finished")
        else:
            "herokuのtmpフォルダの中を確認します"
            for file_name in glob.glob("/tmp/*.*"):
                await self.bot.say(file_name)
            await self.bot.say("Finished")

    @commands.command(pass_context=True)
    async def test(self, ctx):
        "test用だよ。"
        ctx.message.content = "?help"
        await self.bot.process_commands(ctx.message)
    #    self.bot.get_command("help")

    @commands.command(pass_context=True, description="")
    async def bot_logout(self, ctx):
        "簡易版自害プログラム。このbotをlogoutさせます。まだserverには残ります。このserver内のbotのメッセージを100件まで削除します。"
        try:
            ctx.message.content="?delete_bot_messages"
            await self.bot.process_commands(ctx.message)
        finally:
            await self.bot.logout()

    @commands.command(pass_context=True)
    async def bot_kick(self, ctx):
        "本格版自害プログラム。このbotをserverからkickした上でlogoutさせます。このbotのすべてのserverにおけるメッセージを100件まで削除します。"
        try:
            for server in self.bot.servers:  # 全serverで行う
                try:
                    ctx.message.server = server
                    ctx.message.content = "?delete_bot_messages"
                    await self.bot.process_commands(ctx.message)
                finally:
                    await self.bot.leave_server(server)
        finally:
            await self.bot.logout()  # logout

    @commands.command(pass_context=True,description="")
    async def delete_bot_messages(self, ctx):
        "自害プログラムの一部。発言を停止させた上でserver内のbotのメッセージを100件まで削除します。"
        # まずは役職の権限を利用してbotの発言を止める。他のメンバーはpeopleという新役職に避難
        try:
            role_people = await self.bot.create_role(ctx.message.ctx.message.server, name="people", hoist=True)
            role_suicide = await self.bot.create_role(ctx.message.server, name="自害プログラム進行中", hoist=True,send_messages=False,manage_roles=True)
            role_every = await self.bot.discord.utils.get(ctx.message.server.roles, name="@everyone")

            await self.bot.edit_role(ctx.message.server, role_every, send_messages=False) # everyoneの権限を変更してメッセージの送信を不可に。
            for member in ctx.message.server.members:
                if member != self.bot.user:
                    await self.bot.add_roles(member, role_people) # role_peopleにbot以外を移す
            for role in self.bot.user.roles:
                if role != role_suicide:
                    await self.bot.remove_roles(self.bot.user, role)  # role_suicide以外の役職を外す
            # role_suicideを削除
            await self.bot.delete_role(ctx.message.server, role_suicide)
        finally:
            for channel in ctx.message.server.channels: # server内のmessageを削除
                #await self.bot.say(channel.name)
                async for msg in self.bot.logs_from(channel):
                    if msg.author == self.bot.user:
                        await self.bot.delete_message(msg)
            #await self.bot.send_message(channel, "Finished, and I'll be back.") # もう送れない

    @commands.command(pass_context=True, description="")
    async def chsv(self, ctx):
        "change_server。command実行上のserverを変更します。"
        ctx.message.server = self.bot.get_server("413951021891452928")
        ctx.message.author.server = ctx.message.server # 表記一致させないと……

def setup(bot):
    bot.add_cog(System(bot))
