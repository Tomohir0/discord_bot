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

    @commands.command(pass_context=True)
    async def test(self, ctx):
        "test用だよ。"
        ctx.message.content = "?help"
        await self.bot.process_commands(ctx.message)


def setup(bot):
    bot.add_cog(System(bot))
