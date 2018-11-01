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
    "system上存在する関数だよ！new以外はみんなの前ではあまり使われないかも！"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='sourceは https://github.com/Tomohir0/discord_bot/blob/master/shinma.py を確認してください。')
    async def new():
        """最近の更新情報をお知らせします。"""
        m_new = ("Nov,2:cogを導入！開発側としては大分大きいけど、使い手としては関数に分類が付いたくらいかな？関数ごとの説明はまたおいおい"
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
        m2 = ("\n\n過去の更新情報については https://github.com/Tomohir0/discord_bot/blob/master/README ")
        await self.bot.say(m_new + m2)

    @commands.command(description='bot再起動する前に使用して、tmpフォルダ内のファイルが失われるのを防ぎましょう。', pass_context=True)
    async def tmp_up(ctx: commands.Context):
        "tmpフォルダ内のfileをs3に避難させます(upload)。"
        for file_name in glob.glob("/tmp/*.*"):
            await self.bot.say(file_name)
            # "/tmp/"のままではs3においては""(空欄)ディレクトリ内のtmpディレクトリにアクセスしてしまう
            s3.Object(bucket_name, file_name[1:]).upload_file(file_name)
        await self.bot.say("Finished")


    @commands.command(description='bot再起動後に使用して、tmpフォルダ内にあるべきファイルを復活させましょう。', pass_context=True)
    async def tmp_dl(ctx: commands.Context):
        "s3からtmpフォルダにfileを復帰させます。(download)"
        client = boto3.client('s3')
        # "/tmp/"のままではs3においては""(空欄)ディレクトリ内のtmpディレクトリにアクセスしてしまう
        response = client.list_objects(Bucket=bucket_name, Prefix="tmp/")
        file_list = [content['Key'] for content in response['Contents']]
        for file_name in file_list:
            await self.bot.say(file_name)
            s3.Object(bucket_name, file_name).download_file("/"+file_name)
        await self.bot.say("Finished")


def setup(bot):
    bot.add_cog(System(bot))